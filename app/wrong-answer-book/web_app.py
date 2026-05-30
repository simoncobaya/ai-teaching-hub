#!/usr/bin/env python3
"""
web_app.py — 智能错题库 Web 界面

Flask 单页应用，为小朋友提供直观的错题管理界面。
所有业务逻辑复用 WrongAnswerBook 类，无需重写。

启动:
    python web_app.py
    python web_app.py --port 8080 --work-dir /path/to/work
"""

import os
import re
import sys
import io
import json
import uuid
import shutil
import logging
import threading
from pathlib import Path
from datetime import datetime
from contextlib import redirect_stdout
from typing import Optional

from flask import (
    Flask, request, jsonify, send_from_directory,
    render_template, make_response,
)

# ── 确保错误处理无缓存 ──────────────────────────────────
# ═══════════════════════════════════════════════════════════
# 路径 & 导入设置
# ═══════════════════════════════════════════════════════════

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent.parent
_SKILL_SCRIPTS = _PROJECT_ROOT / "skills" / "wrong-answer-book" / "scripts"

sys.path.insert(0, str(_SCRIPT_DIR))
sys.path.insert(0, str(_SKILL_SCRIPTS))

from wrong_answer_book import (  # noqa: E402
    WrongAnswerBook, ImageUtils, MarkdownParser, MarkdownUpdater,
    MarkdownBuilder,
    SUPPORTED_EXTS, MAX_FILE_SIZE, API_MAX_WAIT, API_POLL_INTERVAL,
)
from submit_question_mark import (  # noqa: E402
    load_credentials, submit_job, query_result, parse_response,
)

# ── 日志 ──────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("web_app")


# ═══════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════

def _quiet_call(fn, *args, **kwargs):
    """调用函数但抑制 stdout 输出。"""
    with redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


def _ok(data=None):
    """构造成功 JSON 响应。"""
    return jsonify({"ok": True, "data": data})


def _err(msg, code=400):
    """构造错误 JSON 响应。"""
    resp = jsonify({"ok": False, "error": str(msg)})
    resp.status_code = code
    return resp


def _parse_wrong_blocks(md_path: str) -> list[dict]:
    """
    从 MD 文件中解析所有错题区块（比 MarkdownParser.extract_wrong_table
    更健壮，能处理多行表格单元格）。
    返回列表，每项含 seq, big_question, sub_question, knowledge_points。
    """
    if not os.path.exists(md_path):
        return []
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = []
    for m in re.finditer(
        r"^### 错题 (\d+) — (.+?)(?: ✅ 已掌握)?\n",
        content, re.MULTILINE,
    ):
        seq = int(m.group(1))
        kp_primary = m.group(2).strip()
        start = m.end()

        # 找到当前区块结束位置（下一个 ### 错题 或 ## 标题）
        next_block = re.search(
            r"^### 错题 \d+ |^## ", content[start:], re.MULTILINE,
        )
        end = start + next_block.start() if next_block else len(content)
        block = content[start:end]

        # 提取大题和答错空
        bq = re.search(r"\*\*大题\*\*：(.+?)(?:\n|$)", block)
        sq = re.search(r"\*\*答错空\*\*：(.+?)(?:\n|$)", block)

        blocks.append({
            "seq": seq,
            "big_question": bq.group(1).strip() if bq else "",
            "sub_question": sq.group(1).strip() if sq else "",
            "knowledge_points": kp_primary,
        })

    return blocks


# ═══════════════════════════════════════════════════════════
# 任务管理器（异步分析）
# ═══════════════════════════════════════════════════════════

class TaskManager:
    """内存中的分析任务状态管理（单用户场景，无需持久化）。"""

    def __init__(self):
        self._tasks: dict[str, dict] = {}
        self._lock = threading.Lock()

    def create(self) -> str:
        """创建新任务，返回 task_id。"""
        task_id = uuid.uuid4().hex[:12]
        with self._lock:
            self._tasks[task_id] = {
                "status": "submitted",
                "progress": "正在准备...",
                "result": None,
                "error": None,
                "elapsed": 0,
            }
        return task_id

    def update(self, task_id: str, **kwargs):
        """更新任务状态。"""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].update(kwargs)

    def get(self, task_id: str) -> Optional[dict]:
        """获取任务状态。"""
        with self._lock:
            return self._tasks.get(task_id)

    def cleanup_old(self, max_age: int = 3600):
        """清理超时任务（非关键，仅防内存泄漏）。"""
        pass  # 单用户场景，任务量小，暂不实现


# ═══════════════════════════════════════════════════════════
# 后台分析线程
# ═══════════════════════════════════════════════════════════

def _run_analysis(
    task_id: str,
    image_path: str,
    subject: str,
    grade: str,
    exam_name: str,
    wab: WrongAnswerBook,
    task_mgr: TaskManager,
    overwrite: bool = False,
) -> None:
    """
    后台分析线程：图片校验 → MD5 去重 → 保存 → API → 解析 → 生成 .md → 更新索引。
    通过 task_mgr 实时更新进度供前端轮询。
    """
    try:
        # ── 1. 校验图片 ──
        task_mgr.update(task_id, status="running", progress="正在校验图片...")
        ok, err = ImageUtils.validate(image_path)
        if not ok:
            task_mgr.update(task_id, status="failed", error=err)
            return

        # ── 2. 计算 MD5 ──
        task_mgr.update(task_id, progress="正在计算指纹...")
        md5_hash = ImageUtils.md5(image_path)

        # ── 3. 去重检查 ──
        dup_record = wab.index.find_by_md5(md5_hash)
        if dup_record is not None and not overwrite:
            task_mgr.update(task_id, status="duplicate",
                          error="此试卷已录入过，是否覆盖重新分析？",
                          dup_info={
                              "subject": dup_record.get("subject", ""),
                              "grade": dup_record.get("grade", ""),
                              "exam_name": dup_record.get("exam_name", ""),
                              "created_at": dup_record.get("created_at", ""),
                              "wrong_count": dup_record.get("wrong_count", 0),
                          })
            return

        # ── 4. 检查 credentials ──
        if not wab.cred_path.exists():
            task_mgr.update(task_id, status="failed",
                          error="未找到 credentials.md，请先初始化工作目录。")
            return
        sid, skey = load_credentials(str(wab.cred_path))
        if "<YOUR_SECRET_ID>" in sid or "<YOUR_SECRET_KEY>" in skey:
            task_mgr.update(task_id, status="failed",
                          error="credentials.md 中仍为占位符，请填入真实的密钥。")
            return

        # ── 5. 保存图片 ──
        task_mgr.update(task_id, progress="正在保存图片...")
        ext = Path(image_path).suffix.lower()
        img_filename = f"{md5_hash}{ext}"
        img_abs = wab.images_dir / img_filename
        ImageUtils.save(image_path, str(img_abs))
        img_rel = f"images/{img_filename}"

        # ── 6. 调用 API ──
        task_mgr.update(task_id, progress="正在提交批改任务...", elapsed=0)
        start = datetime.now()

        job_id = submit_job(image_path, sid, skey)

        task_mgr.update(task_id, progress="正在等待批改结果（最长 120 秒）...")
        mark_infos = query_result(job_id, sid, skey, API_MAX_WAIT, API_POLL_INTERVAL)

        elapsed = int((datetime.now() - start).total_seconds())
        task_mgr.update(task_id, progress=f"批改完成，耗时 {elapsed} 秒", elapsed=elapsed)

        # ── 7. 解析错题 ──
        task_mgr.update(task_id, progress="正在解析错题...")
        wrong_items = parse_response(mark_infos)
        total_qs = sum(len(q.MarkInfos or []) for q in mark_infos)

        if not wrong_items:
            task_mgr.update(task_id, status="done",
                          progress="🎉 没有发现错题，太棒了！",
                          result={"wrong_count": 0, "total_questions": total_qs})
            return

        # ── 8. 推断元信息 ──
        if not subject:
            subject = WrongAnswerBook._infer_subject(mark_infos, wrong_items)
        if not grade:
            grade = WrongAnswerBook._infer_grade(mark_infos, wrong_items)

        # ── 9. 生成 Markdown ──
        task_mgr.update(task_id, progress="正在生成错题库...")
        created_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        old_mastered: list[int] = []
        if overwrite and dup_record:
            old_mastered = dup_record.get("mastered", [])

        md_content = MarkdownBuilder.build(
            subject=subject,
            grade=grade,
            exam_name=exam_name,
            total_questions=total_qs,
            wrong_items=wrong_items,
            image_rel_path=img_rel,
            created_at=created_at,
            mastered=old_mastered if overwrite else [],
        )

        file_name = f"错题库_{grade}{subject}"
        if exam_name:
            file_name += f"_{exam_name}"
        file_name += ".md"
        md_path = wab.wab_dir / file_name
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # ── 10. 更新索引 ──
        task_mgr.update(task_id, progress="正在更新索引...")
        record = {
            "md5": md5_hash,
            "image": img_rel,
            "file": file_name,
            "subject": subject,
            "grade": grade,
            "exam_name": exam_name,
            "wrong_count": len(wrong_items),
            "total_questions": total_qs,
            "mastered": old_mastered if overwrite else [],
            "created_at": created_at,
        }

        if overwrite and dup_record:
            for i, r in enumerate(wab.index.records):
                if r.get("md5") == md5_hash:
                    wab.index.update(i, record)
                    break
        else:
            wab.index.add(record)

        # ── Done ──
        task_mgr.update(task_id, status="done",
                      progress=f"✅ 完成！发现 {len(wrong_items)} 道错题",
                      result={
                          "wrong_count": len(wrong_items),
                          "total_questions": total_qs,
                          "subject": subject,
                          "grade": grade,
                          "exam_name": exam_name,
                          "file": file_name,
                          "elapsed": elapsed,
                      })

    except Exception as e:
        log.exception(f"分析任务 {task_id} 失败")
        task_mgr.update(task_id, status="failed", error=str(e))


# ═══════════════════════════════════════════════════════════
# Web 专用删除（绕过 CLI 的 input() 交互确认）
# ═══════════════════════════════════════════════════════════

def _web_delete_exam(ref: str, wab: WrongAnswerBook) -> None:
    """直接删除整份试卷（无交互）。"""
    rec_idx = int(ref) - 1
    valid = wab.index.valid_records()
    if rec_idx < 0 or rec_idx >= len(valid):
        raise ValueError(f"无效编号: [{ref}]")
    vi, rec = valid[rec_idx]

    # 删除 md 文件
    md_path = wab.wab_dir / rec["file"]
    if md_path.exists():
        md_path.unlink()
    # 删除图片
    img_path = wab.wab_dir / rec["image"]
    if img_path.exists():
        img_path.unlink()
    # 删除索引
    wab.index.remove(vi)


def _web_delete_single(ref: str, wab: WrongAnswerBook) -> None:
    """直接删除单个错题（无交互，不再追问是否删除空试卷）。"""
    rec_num, seq_str = ref.split(".", 1)
    rec_idx = int(rec_num) - 1
    seq = int(seq_str)

    valid = wab.index.valid_records()
    if rec_idx < 0 or rec_idx >= len(valid):
        raise ValueError(f"无效编号: [{rec_num}]")
    vi, rec = valid[rec_idx]

    md_path = wab.wab_dir / rec["file"]
    new_count = MarkdownUpdater.remove_wrong_item(str(md_path), seq)

    # 更新索引
    rec["wrong_count"] = new_count
    mastered = [s for s in rec.get("mastered", []) if s != seq]
    mastered = [(s - 1 if s > seq else s) for s in mastered]
    rec["mastered"] = mastered
    wab.index.update(vi, rec)


# ═══════════════════════════════════════════════════════════
# Flask 应用工厂
# ═══════════════════════════════════════════════════════════

def create_app(work_dir: str = ".") -> Flask:
    """创建并配置 Flask 应用。"""
    app = Flask(__name__,
                template_folder=str(_SCRIPT_DIR / "templates"))
    app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

    wab = WrongAnswerBook(work_dir=work_dir)
    task_mgr = TaskManager()

    # ── 前端页面 ────────────────────────────────────────

    @app.route("/")
    def index():
        """渲染单页前端。"""
        return render_template("index.html")

    # ── 图片服务 ────────────────────────────────────────

    @app.route("/images/<path:filename>")
    def serve_image(filename: str):
        """提供试卷图片文件。"""
        return send_from_directory(str(wab.images_dir), filename)

    # ── 初始化相关 ──────────────────────────────────────

    @app.route("/api/init-status")
    def api_init_status():
        """检查是否已初始化：credentials 和目录是否存在。"""
        has_cred = wab.cred_path.exists()
        has_index = wab.index_path.exists()
        return _ok({
            "initialized": has_cred and has_index,
            "has_credentials": has_cred,
            "has_index": has_index,
            "wab_dir": str(wab.wab_dir),
        })

    @app.route("/api/init", methods=["POST"])
    def api_init():
        """初始化工作目录。"""
        try:
            _quiet_call(wab.cmd_init, force=False)
            return _ok({"message": "初始化成功"})
        except Exception as e:
            return _err(f"初始化失败: {e}")

    # ── 试卷分析（异步） ────────────────────────────────

    @app.route("/api/analyze", methods=["POST"])
    def api_analyze():
        """提交试卷分析任务。"""
        if "image" not in request.files:
            return _err("请上传试卷图片")

        file = request.files["image"]
        if not file.filename:
            return _err("未选择文件")

        # 校验扩展名
        ext = Path(file.filename).suffix.lower()
        if ext not in SUPPORTED_EXTS:
            return _err(f"不支持的图片格式: {ext}，支持: {', '.join(SUPPORTED_EXTS)}")

        # 保存到临时文件
        tmp_dir = wab.wab_dir / ".tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        tmp_path = tmp_dir / f"upload_{uuid.uuid4().hex[:8]}{ext}"
        file.save(str(tmp_path))

        # 校验
        ok, err = ImageUtils.validate(str(tmp_path))
        if not ok:
            tmp_path.unlink(missing_ok=True)
            return _err(err)

        # 读取表单参数
        subject = request.form.get("subject", "").strip()
        grade = request.form.get("grade", "").strip()
        exam_name = request.form.get("exam_name", "").strip()
        overwrite = request.form.get("overwrite", "false").lower() == "true"

        # 创建任务
        task_id = task_mgr.create()

        # 存储元信息供覆盖重试使用
        task_mgr.update(task_id,
                        image_path=str(tmp_path),
                        subject=subject,
                        grade=grade,
                        exam_name=exam_name)

        # 启动后台线程
        t = threading.Thread(
            target=_run_analysis,
            args=(task_id, str(tmp_path), subject, grade, exam_name, wab, task_mgr),
            kwargs={"overwrite": overwrite},
            daemon=True,
        )
        t.start()

        return _ok({"task_id": task_id})

    @app.route("/api/task/<task_id>")
    def api_task(task_id: str):
        """查询分析任务状态。"""
        task = task_mgr.get(task_id)
        if task is None:
            return _err("任务不存在", 404)
        return _ok(task)

    @app.route("/api/task/<task_id>/overwrite", methods=["POST"])
    def api_task_overwrite(task_id: str):
        """确认覆盖已存在的试卷，重新提交分析（不重新上传图片）。"""
        task = task_mgr.get(task_id)
        if not task or task.get("status") != "duplicate":
            return _err("无效的覆盖请求，任务状态不匹配")
        image_path = task.get("image_path", "")
        if not image_path or not os.path.exists(image_path):
            return _err("临时文件已过期，请重新上传试卷")

        # 重置任务状态
        task_mgr.update(task_id, status="submitted",
                        progress="正在重新分析...", error=None,
                        dup_info=None)

        # 启动后台线程（overwrite=True 跳过去重拦截）
        t = threading.Thread(
            target=_run_analysis,
            args=(task_id, image_path,
                  task.get("subject", ""),
                  task.get("grade", ""),
                  task.get("exam_name", ""),
                  wab, task_mgr),
            kwargs={"overwrite": True},
            daemon=True,
        )
        t.start()
        return _ok({"task_id": task_id})

    # ── 错题记录 ─────────────────────────────────────────

    @app.route("/api/records")
    def api_records():
        """获取所有错题记录（含单题列表）。"""
        try:
            valid = wab.index.valid_records()
            result = []
            for display_num, (vi, rec) in enumerate(valid, 1):
                mastered = rec.get("mastered", [])
                item = {
                    "num": display_num,
                    "index": vi,
                    "md5": rec.get("md5", ""),
                    "image": rec.get("image", ""),
                    "file": rec.get("file", ""),
                    "subject": rec.get("subject", ""),
                    "grade": rec.get("grade", ""),
                    "exam_name": rec.get("exam_name", ""),
                    "wrong_count": rec.get("wrong_count", 0),
                    "total_questions": rec.get("total_questions", 0),
                    "mastered": mastered,
                    "mastered_count": len(mastered),
                    "created_at": rec.get("created_at", ""),
                }

                # 从 MD 读取错题列表（使用健壮的区块解析器）
                md_path = wab.wab_dir / rec.get("file", "")
                if md_path.exists():
                    blocks = _parse_wrong_blocks(str(md_path))
                    items_list = []
                    for blk in blocks:
                        blk["mastered"] = blk["seq"] in mastered
                        items_list.append(blk)
                    item["wrong_items"] = items_list
                else:
                    item["wrong_items"] = []

                result.append(item)

            return _ok(result)
        except Exception as e:
            log.exception("获取记录失败")
            return _err(f"获取记录失败: {e}")

    @app.route("/api/view/<ref>")
    def api_view(ref: str):
        """查看试卷或单题详情。"""
        try:
            if "." in ref:
                rec_num, seq_str = ref.split(".", 1)
                rec_idx = int(rec_num) - 1
                seq = int(seq_str)
                single = True
            else:
                rec_idx = int(ref) - 1
                seq = 0
                single = False

            valid = wab.index.valid_records()
            if rec_idx < 0 or rec_idx >= len(valid):
                return _err(f"无效编号: [{ref}]")

            vi, rec = valid[rec_idx]

            if single:
                md_path = wab.wab_dir / rec["file"]
                details = MarkdownParser.extract_wrong_details(str(md_path), seq)
                if details is None:
                    return _err(f"未找到错题 {ref}")

                details["mastered"] = seq in rec.get("mastered", [])
                details["num"] = rec_idx + 1
                details["ref"] = ref
                details["exam_info"] = {
                    "grade": rec.get("grade", ""),
                    "subject": rec.get("subject", ""),
                    "exam_name": rec.get("exam_name", ""),
                }
                return _ok(details)
            else:
                # 返回整份试卷的索引信息 + 所有错题详情
                md_path = wab.wab_dir / rec["file"]
                from wrong_answer_book import MarkdownParser as MP
                table_rows = MP.extract_wrong_table(str(md_path))
                mastered = rec.get("mastered", [])
                items = []
                for row in table_rows:
                    s = row["序号"]
                    items.append({
                        "seq": s,
                        "big_question": row["大题"],
                        "sub_question": row["小题"],
                        "knowledge_points": row["知识点"],
                        "mastered": s in mastered,
                    })
                return _ok({
                    "num": vi + 1,
                    "grade": rec.get("grade", ""),
                    "subject": rec.get("subject", ""),
                    "exam_name": rec.get("exam_name", ""),
                    "wrong_count": rec.get("wrong_count", 0),
                    "total_questions": rec.get("total_questions", 0),
                    "created_at": rec.get("created_at", ""),
                    "image": rec.get("image", ""),
                    "items": items,
                })

        except Exception as e:
            log.exception(f"查看记录失败: {ref}")
            return _err(f"查看失败: {e}")

    # ── 统计 ─────────────────────────────────────────────

    @app.route("/api/stats")
    def api_stats():
        """获取统计数据。"""
        try:
            records = wab.index.records
            if not records:
                return _ok({
                    "exam_count": 0,
                    "total_wrong": 0,
                    "total_questions": 0,
                    "total_mastered": 0,
                    "by_subject": {},
                    "by_grade": {},
                })

            total_wrong = sum(r.get("wrong_count", 0) for r in records)
            total_qs = sum(r.get("total_questions", 0) for r in records)
            total_mastered = sum(len(r.get("mastered", [])) for r in records)

            by_subject: dict = {}
            for r in records:
                sub = r.get("subject", "未知")
                if sub not in by_subject:
                    by_subject[sub] = {"wrong": 0, "mastered": 0, "count": 0}
                by_subject[sub]["wrong"] += r.get("wrong_count", 0)
                by_subject[sub]["mastered"] += len(r.get("mastered", []))
                by_subject[sub]["count"] += 1

            by_grade: dict = {}
            for r in records:
                gd = r.get("grade", "未知")
                if gd not in by_grade:
                    by_grade[gd] = {"wrong": 0, "mastered": 0, "count": 0}
                by_grade[gd]["wrong"] += r.get("wrong_count", 0)
                by_grade[gd]["mastered"] += len(r.get("mastered", []))
                by_grade[gd]["count"] += 1

            return _ok({
                "exam_count": len(records),
                "total_wrong": total_wrong,
                "total_questions": total_qs,
                "total_mastered": total_mastered,
                "unmastered": total_wrong - total_mastered,
                "mastery_rate": round(total_mastered / total_wrong * 100) if total_wrong > 0 else 0,
                "by_subject": by_subject,
                "by_grade": by_grade,
            })
        except Exception as e:
            log.exception("获取统计失败")
            return _err(f"获取统计失败: {e}")

    # ── 掌握标记 ─────────────────────────────────────────

    @app.route("/api/master/<ref>", methods=["POST"])
    def api_master(ref: str):
        """标记单题为已掌握。"""
        try:
            _quiet_call(wab.cmd_master, ref)
            return _ok({"message": f"已标记 {ref} 为已掌握"})
        except SystemExit:
            return _err("操作失败，请检查编号是否正确")
        except Exception as e:
            log.exception(f"标记掌握失败: {ref}")
            return _err(f"操作失败: {e}")

    @app.route("/api/unmaster/<ref>", methods=["POST"])
    def api_unmaster(ref: str):
        """取消已掌握标记。"""
        try:
            _quiet_call(wab.cmd_unmaster, ref)
            return _ok({"message": f"已取消 {ref} 的掌握标记"})
        except SystemExit:
            return _err("操作失败，请检查编号是否正确")
        except Exception as e:
            log.exception(f"取消掌握失败: {ref}")
            return _err(f"操作失败: {e}")

    # ── 删除 ─────────────────────────────────────────────

    @app.route("/api/delete/<ref>", methods=["DELETE"])
    def api_delete(ref: str):
        """删除试卷或单题记录（无需交互确认，由前端弹窗确认）。"""
        try:
            if "." in ref:
                _web_delete_single(ref, wab)
            else:
                _web_delete_exam(ref, wab)
            return _ok({"message": f"已删除 {ref}"})
        except ValueError as e:
            return _err(str(e))
        except Exception as e:
            log.exception(f"删除失败: {ref}")
            return _err(f"删除失败: {e}")

    # ── 错误处理 ─────────────────────────────────────────

    @app.errorhandler(413)
    def too_large(e):
        return _err("文件太大了，请选择 10MB 以内的图片", 413)

    @app.errorhandler(404)
    def not_found(e):
        return _err("页面不存在", 404)

    @app.errorhandler(500)
    def server_error(e):
        return _err("服务器内部错误", 500)

    # ── 无缓存头 ─────────────────────────────────────────

    @app.after_request
    def no_cache(response):
        """API 响应禁用缓存。"""
        if request.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        return response

    return app


# ═══════════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="智能错题库 Web 界面")
    parser.add_argument("--port", type=int, default=5000, help="服务端口（默认 5000）")
    parser.add_argument("--host", default="127.0.0.1", help="绑定地址（默认 127.0.0.1）")
    parser.add_argument("--work-dir", default=".", help="工作目录（默认当前目录）")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    args = parser.parse_args()

    app = create_app(work_dir=args.work_dir)

    print("")
    print("  📚  智能错题库 Web 版")
    print(f"  🌐  地址: http://{args.host}:{args.port}")
    print(f"  📂  工作目录: {Path(args.work_dir).resolve()}")
    print("")
    print("  按 Ctrl+C 停止服务")
    print("")

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
