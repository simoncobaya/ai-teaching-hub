#!/usr/bin/env python3
"""
wrong_answer_book.py — 智能错题库 CLI 工具

将试卷图片自动识别为错题记录，支持查询、统计、掌握标记和删除。
脱离 CodeBuddy 环境，任何 Python 3.8+ 均可运行。

用法:
    python wrong_answer_book.py init                 # 初始化工作目录
    python wrong_answer_book.py analyze <图片路径>    # 分析试卷
    python wrong_answer_book.py list                 # 列出错题
    python wrong_answer_book.py view <编号>           # 查看详情
    python wrong_answer_book.py stats                # 统计汇总
    python wrong_answer_book.py master <编号>         # 标记已掌握
    python wrong_answer_book.py unmaster <编号>       # 取消掌握
    python wrong_answer_book.py delete <编号>         # 删除记录
"""

import sys
import os
import json
import hashlib
import argparse
import shutil
import re
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

# ── 动态添加 submit_question_mark.py 所在路径 ──────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent.parent
_SKILL_SCRIPTS = _PROJECT_ROOT / "skills" / "wrong-answer-book" / "scripts"
_SKILL_ASSETS = _PROJECT_ROOT / "skills" / "wrong-answer-book" / "assets"

sys.path.insert(0, str(_SKILL_SCRIPTS))
from submit_question_mark import (  # noqa: E402
    load_credentials,
    submit_job,
    query_result,
    parse_response,
)

# ── 可选依赖 ───────────────────────────────────────────────────────────
try:
    from PIL import Image

    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ── 常量 ───────────────────────────────────────────────────────────────
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
API_MAX_WAIT = 120  # 秒
API_POLL_INTERVAL = 3  # 秒


# ═══════════════════════════════════════════════════════════════════════
# 图片工具类
# ═══════════════════════════════════════════════════════════════════════

class ImageUtils:
    """图片校验、MD5 计算与保存。"""

    @staticmethod
    def validate(image_path: str) -> tuple[bool, str]:
        """
        校验图片格式和大小。
        返回 (是否通过, 错误信息)。
        """
        p = Path(image_path)
        if not p.exists():
            return False, f"文件不存在: {image_path}"
        if not p.is_file():
            return False, f"路径不是文件: {image_path}"

        ext = p.suffix.lower()
        if ext not in SUPPORTED_EXTS:
            return False, f"不支持的图片格式: {ext}，支持: {', '.join(SUPPORTED_EXTS)}"

        size = p.stat().st_size
        if size > MAX_FILE_SIZE:
            return False, f"文件大小 {size / 1024 / 1024:.1f}MB 超过限制 10MB"

        if HAS_PIL:
            try:
                with Image.open(image_path) as img:
                    img.verify()
            except Exception as e:
                return False, f"图片校验失败: {e}"
        return True, ""

    @staticmethod
    def md5(image_path: str) -> str:
        """计算文件的 MD5 哈希值。"""
        h = hashlib.md5()
        with open(image_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def save(src_path: str, dst_path: str) -> str:
        """复制图片到目标路径，返回目标路径字符串。"""
        Path(dst_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        return dst_path


# ═══════════════════════════════════════════════════════════════════════
# 索引管理类
# ═══════════════════════════════════════════════════════════════════════

class IndexManager:
    """.index.json 读写与查询。"""

    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.records: list[dict] = self._load()

    def _load(self) -> list[dict]:
        """从文件加载索引记录。"""
        if not self.index_path.exists():
            return []
        try:
            with open(self.index_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []

    def save(self) -> None:
        """将索引记录写回文件。"""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)

    def find_by_md5(self, md5: str) -> Optional[dict]:
        """按 MD5 查找记录，返回记录或 None。"""
        for r in self.records:
            if r.get("md5") == md5:
                return r
        return None

    def add(self, record: dict) -> None:
        """追加一条记录到索引。"""
        self.records.append(record)
        self.save()

    def update(self, idx: int, record: dict) -> None:
        """更新指定位置的记录（0-based）。"""
        if 0 <= idx < len(self.records):
            self.records[idx] = record
            self.save()

    def remove(self, idx: int) -> dict:
        """删除并返回指定位置的记录（0-based）。"""
        if 0 <= idx < len(self.records):
            removed = self.records.pop(idx)
            self.save()
            return removed
        raise IndexError(f"索引序号 {idx} 无效，共 {len(self.records)} 条记录")

    def valid_records(self) -> list[tuple[int, dict]]:
        """返回 (索引, 记录) 的列表，仅包含 wrong_count > 0 的记录。"""
        return [(i, r) for i, r in enumerate(self.records) if r.get("wrong_count", 0) > 0]


# ═══════════════════════════════════════════════════════════════════════
# Markdown 构建器
# ═══════════════════════════════════════════════════════════════════════

class MarkdownBuilder:
    """按模板生成错题库 Markdown 文件。"""

    @staticmethod
    def build(
        subject: str,
        grade: str,
        exam_name: str,
        total_questions: int,
        wrong_items: list[dict],
        image_rel_path: str,
        created_at: str,
        mastered: Optional[list[int]] = None,
    ) -> str:
        """
        构建完整的错题库 Markdown 字符串。

        params:
            subject / grade / exam_name — 试卷元信息
            total_questions — 总题数
            wrong_items — 错题列表，每项含 big_question, sub_question,
                          handwrite, analysis, right_answer, knowledge_points
            image_rel_path — 图片相对路径（如 images/abc.jpg）
            created_at — 录入时间（ISO 8601）
            mastered — 已掌握序号列表（1-based）
        """
        mastered = mastered or []
        wrong_count = len(wrong_items)
        lines: list[str] = []

        # ── 1. 文档头部 ──
        title = f"{grade}{subject}"
        if exam_name:
            title += f" {exam_name}"
        lines.append(f"# 错题库 — {title}")
        lines.append("")
        lines.append(f"> **录入时间**：{created_at}")
        if exam_name:
            lines.append(f"> **试卷**：{grade}{subject} {exam_name}")
        lines.append(f"> **总题数**：{total_questions} 道 | **错题数**：{wrong_count} 道")
        lines.append("")
        lines.append("---")
        lines.append("")

        # ── 2. 错题统计 ──
        lines.append("## 错题统计")
        lines.append("")
        lines.append("| 序号 | 大题 | 小题 | 知识点 | 作答 | 状态 |")
        lines.append("|:---:|------|------|--------|:---:|:---:|")
        for i, item in enumerate(wrong_items, 1):
            bq = item.get("big_question", "") or ""
            sq = item.get("sub_question", "") or ""
            kp = ", ".join(item.get("knowledge_points", [])[:2]) or "—"
            status = "✅ 已掌握" if i in mastered else "—"
            lines.append(f"| {i} | {bq} | {sq} | {kp} | ❌ | {status} |")
        lines.append("")

        # 薄弱知识点分布
        kp_count: dict[str, int] = {}
        for item in wrong_items:
            for kp in item.get("knowledge_points", []):
                kp_count[kp] = kp_count.get(kp, 0) + 1
        if kp_count:
            lines.append("**薄弱知识点分布**：")
            lines.append("")
            lines.append("| 知识点 | 错题数 |")
            lines.append("|--------|:---:|")
            for kp, cnt in sorted(kp_count.items(), key=lambda x: -x[1]):
                lines.append(f"| {kp} | {cnt} |")
        lines.append("")
        lines.append("---")
        lines.append("")

        # ── 3. 错题逐题分析 ──
        for i, item in enumerate(wrong_items, 1):
            bq = item.get("big_question", "")
            sq = item.get("sub_question", "")
            kp_list = item.get("knowledge_points", [])
            kp_primary = kp_list[0] if kp_list else "未知知识点"
            ans = item.get("handwrite", "")
            right = item.get("right_answer", "")
            analysis = item.get("analysis", "")
            mastered_suffix = " ✅ 已掌握" if i in mastered else ""

            lines.append(f"### 错题 {i} — {kp_primary}{mastered_suffix}")
            lines.append("")
            if bq:
                lines.append(f"**大题**：{bq}")
                lines.append("")
            if bq:
                lines.append("**原题**：")
                lines.append(f"> {bq}")
                lines.append("")
            if sq:
                lines.append(f"**答错空**：{sq}")
                lines.append("")
            lines.append("| 项目 | 内容 |")
            lines.append("|------|------|")
            lines.append(f"| **我的答案** | {ans} |")
            lines.append(f"| **正确答案** | {right} |")
            lines.append(f"| **错误原因** | {analysis} |")
            lines.append("")

            # 订正建议（简单版：从分析中截取）
            lines.append(f"> 💡 **订正**：{analysis}")
            lines.append("")
            if kp_list:
                tags = " ".join(f"`#{kp}`" for kp in kp_list)
                lines.append(f"**知识点标签**：{tags}")
                lines.append("")
            lines.append("---")
            lines.append("")

        # ── 4. 薄弱知识点诊断 ──
        lines.append("## 薄弱知识点诊断")
        lines.append("")
        if kp_count:
            lines.append("| 薄弱点 | 严重程度 | 说明 |")
            lines.append("|--------|:---:|------|")
            for kp, cnt in sorted(kp_count.items(), key=lambda x: -x[1]):
                severity = "🔴 高" if cnt >= 2 else "🟡 中"
                desc = f"{cnt} 道" + ("，需重点加强" if cnt >= 2 else "")
                lines.append(f"| {kp} | {severity} | {desc} |")
        else:
            lines.append("（无显著薄弱点）")
        lines.append("")
        lines.append("---")
        lines.append("")

        # ── 5. 巩固练习建议 ──
        lines.append("## 巩固练习建议")
        lines.append("")
        if kp_count:
            for kp in sorted(kp_count, key=lambda x: -kp_count[x])[:3]:
                lines.append(f"### {kp}专项")
                lines.append("")
                lines.append(f"1. 针对「{kp}」知识点进行专项训练")
                lines.append(f"2. 整理错题笔记，归纳常见错误类型")
                lines.append("")
        else:
            lines.append("建议定期复习错题本中的内容。")
        lines.append("---")
        lines.append("")

        # ── 6. 原始试卷图片 ──
        lines.append("## 📷 原始试卷")
        lines.append("")
        lines.append(f"![试卷图片]({image_rel_path})")
        lines.append("")
        lines.append("> 可对照回顾完整试卷内容。")
        lines.append("")
        lines.append("---")
        lines.append("")

        # ── 7. 文档尾部 ──
        lines.append("*本文件由「智能错题库」自动生成*")
        lines.append("")

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════
# Markdown 解析器
# ═══════════════════════════════════════════════════════════════════════

class MarkdownParser:
    """解析错题库 .md 文件，提取表格和错题详情。"""

    @staticmethod
    def extract_wrong_table(md_path: str) -> list[dict]:
        """
        提取「错题统计」表格的每一行。
        返回列表，每项为 {序号, 大题, 小题, 知识点, 状态}。
        """
        rows: list[dict] = []
        if not os.path.exists(md_path):
            return rows
        with open(md_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        in_table = False
        for line in lines:
            s = line.strip()
            if s.startswith("| 序号 | 大题"):
                in_table = True
                continue
            if in_table:
                if s.startswith("|") and not s.startswith("|:---") and "序号" not in s:
                    parts = [p.strip() for p in s.split("|")[1:-1]]
                    if len(parts) >= 5:
                        try:
                            seq = int(parts[0])
                        except ValueError:
                            continue
                        rows.append({
                            "序号": seq,
                            "大题": parts[1],
                            "小题": parts[2],
                            "知识点": parts[3],
                            "状态": parts[5] if len(parts) > 5 else "—",
                        })
                elif s.startswith("---") or s.startswith("**") or s == "":
                    # 表格结束条件：空行、分隔线或加粗文本
                    if not s.startswith("|"):
                        break
        return rows

    @staticmethod
    def extract_wrong_details(md_path: str, seq: int) -> Optional[dict]:
        """
        提取指定序号的错题详情。
        返回包含大题、原题、答错空、我的答案、正确答案、错误原因 的字典。
        """
        if not os.path.exists(md_path):
            return None
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 定位目标错题区块
        pattern = rf"### 错题 {seq} — .+"
        m = re.search(pattern, content)
        if not m:
            return None

        start = m.start()
        # 查找下一个 ### 错题 或者 ## 标题作为结束
        next_pattern = re.compile(r"^### 错题 |^## ", re.MULTILINE)
        nm = next_pattern.search(content, m.end())
        end = nm.start() if nm else len(content)
        block = content[start:end]

        def _extract_field(field: str) -> str:
            rr = re.search(rf"\*\*{field}\*\*：(.+?)(?:\n|$)", block)
            return rr.group(1).strip() if rr else ""

        def _extract_table_field(field: str) -> str:
            rr = re.search(
                rf"\|\s*\*\*{field}\*\*\s*\|\s*(.+?)\s*\|", block
            )
            return rr.group(1).strip() if rr else ""

        return {
            "大题": _extract_field("大题"),
            "答错空": _extract_field("答错空"),
            "我的答案": _extract_table_field("我的答案"),
            "正确答案": _extract_table_field("正确答案"),
            "错误原因": _extract_table_field("错误原因"),
            "原题": _extract_field("原题") or "",
        }

    @staticmethod
    def count_wrong_items(md_path: str) -> int:
        """统计 .md 文件中的错题数（通过 ### 错题 标题）。"""
        if not os.path.exists(md_path):
            return 0
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        return len(re.findall(r"^### 错题 \d+", content, re.MULTILINE))


# ═══════════════════════════════════════════════════════════════════════
# Markdown 更新器
# ═══════════════════════════════════════════════════════════════════════

class MarkdownUpdater:
    """更新 .md 文件中的状态标记和内容。"""

    @staticmethod
    def update_mastery(md_path: str, seq: int, mastered: bool) -> None:
        """
        在 .md 中更新指定序号的掌握状态。
        mastered=True → 标记为 ✅ 已掌握
        mastered=False → 取消标记，恢复为 —
        """
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. 更新错题统计表格的状态列
        #    匹配: | seq | ... | ❌ | — |
        #    或:   | seq | ... | ❌ | ✅ 已掌握 |
        if mastered:
            content = re.sub(
                rf"^(\| {seq} \|.+?\| ❌ \|) —(\s*\|)",
                r"\g<1> ✅ 已掌握\g<2>",
                content,
                flags=re.MULTILINE,
            )
        else:
            content = re.sub(
                rf"^(\| {seq} \|.+?\| ❌ \|) ✅ 已掌握(\s*\|)",
                r"\g<1> —\g<2>",
                content,
                flags=re.MULTILINE,
            )

        # 2. 更新 ### 错题 {seq} 标题
        title_pat = rf"^(### 错题 {seq} — .+?)( ✅ 已掌握)?$"
        if mastered:
            # 添加 ✅ 已掌握
            content = re.sub(
                title_pat,
                lambda m: m.group(1) + " ✅ 已掌握",
                content,
                flags=re.MULTILINE,
            )
        else:
            # 移除 ✅ 已掌握
            content = re.sub(
                title_pat,
                r"\g<1>",
                content,
                flags=re.MULTILINE,
            )

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def remove_wrong_item(md_path: str, seq: int) -> int:
        """
        从 .md 中移除指定序号的错题区块，并重新编号后续错题。
        返回移除后的错题总数。
        """
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 找到对应的 ### 错题 {seq} — ... 区块
        section_pat = re.compile(
            rf"^---\n\n### 错题 {seq} — .+?^(?=---\n\n### 错题 \d+|---\n\n## )",
            re.MULTILINE | re.DOTALL,
        )
        m = section_pat.search(content)
        if not m:
            # 尝试匹配最后一个错题区块
            section_pat_last = re.compile(
                rf"^---\n\n### 错题 {seq} — .+?(?=---\n\n## |\n\n## )",
                re.MULTILINE | re.DOTALL,
            )
            m = section_pat_last.search(content)
        if not m:
            raise ValueError(f"未找到错题 {seq} 的区块")

        removed_block = m.group()
        content = content.replace(removed_block, "", 1)

        # 重新编号后续错题
        for i in range(seq + 1, 100):
            old_pat = f"### 错题 {i} —"
            new_pat = f"### 错题 {i - 1} —"
            if old_pat in content:
                content = content.replace(old_pat, new_pat)
            else:
                break

        # 重新编号统计表格
        # 更新表格序号后面的行
        lines = content.split("\n")
        new_lines = []
        table_section = False
        seq_offset = 0
        for line in lines:
            s = line.strip()
            if "| 序号 | 大题" in s:
                table_section = True
                new_lines.append(line)
                continue
            if table_section:
                if s.startswith("|:---"):
                    new_lines.append(line)
                    continue
                if s.startswith("| ") and not s.startswith("|:---") and "序号" not in s:
                    parts = s.split("|")
                    try:
                        cur_seq = int(parts[1].strip())
                        if cur_seq == seq:
                            continue  # 跳过被删除的行
                        if cur_seq > seq:
                            parts[1] = parts[1].replace(str(cur_seq), str(cur_seq - 1), 1)
                            new_lines.append("|".join(parts))
                            continue
                    except (ValueError, IndexError):
                        pass
                elif not s.startswith("|"):
                    table_section = False
            new_lines.append(line)

        content = "\n".join(new_lines)

        # 更新错题数
        wrong_count = MarkdownParser.count_wrong_items(
            md_path
        )  # 这需要重新读取，但我们用内容计算
        # 用内容计算
        new_wrong_count = len(
            re.findall(r"^### 错题 \d+", content, re.MULTILINE)
        )

        # 更新头部错题数
        content = re.sub(
            r"\*\*错题数\*\*：\d+ 道",
            f"**错题数**：{new_wrong_count} 道",
            content,
        )

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content)

        return new_wrong_count


# ═══════════════════════════════════════════════════════════════════════
# 主业务类
# ═══════════════════════════════════════════════════════════════════════

class WrongAnswerBook:
    """智能错题库核心业务逻辑。"""

    def __init__(self, work_dir: str = "."):
        self.work_dir = Path(work_dir).resolve()
        self.wab_dir = self.work_dir / "wrong-answer-book"
        self.images_dir = self.wab_dir / "images"
        self.index_path = self.wab_dir / ".index.json"
        self.cred_path = self.work_dir / "credentials.md"
        self.index = IndexManager(self.index_path)

    # ── init ───────────────────────────────────────────────────────

    def cmd_init(self, force: bool = False) -> None:
        """初始化工作目录：创建目录结构，复制 credentials 模板。"""
        self.wab_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)

        print(f"✅ 已创建目录: {self.wab_dir}")
        print(f"✅ 已创建目录: {self.images_dir}")

        if self.index_path.exists():
            print(f"📋 索引文件已存在: {self.index_path}")
            if force:
                print("   已存在，跳过覆盖。")
        else:
            self.index.save()
            print(f"✅ 已初始化索引: {self.index_path}")

        if self.cred_path.exists() and not force:
            print(f"📋 credentials 文件已存在: {self.cred_path}")
        else:
            cred_template = _SKILL_ASSETS / ".credentials.md"
            if cred_template.exists():
                shutil.copy(cred_template, self.cred_path)
                print(f"✅ 已复制 credentials 模板到: {self.cred_path}")
                print(  "   ⚠️  请编辑该文件，填入真实的 SecretId 和 SecretKey")
            else:
                print("⚠️  未找到 credentials 模板，请手动创建 credentials.md")

    # ── analyze ────────────────────────────────────────────────────

    def cmd_analyze(
        self,
        image_path: str,
        subject: str = "",
        grade: str = "",
        exam_name: str = "",
    ) -> None:
        """
        完整分析管道：
        图片校验 → MD5 去重 → 保存图片 → 调用 API → 解析错题 → 生成 Markdown → 更新索引
        """
        # 检查 credentials
        if not self.cred_path.exists():
            print("❌ 未找到 credentials.md，请先运行: python wrong_answer_book.py init")
            sys.exit(1)
        sid, skey = load_credentials(str(self.cred_path))
        if "<YOUR_SECRET_ID>" in sid or "<YOUR_SECRET_KEY>" in skey:
            print("❌ credentials.md 中仍为占位符，请填入真实的 SecretId 和 SecretKey")
            sys.exit(1)

        # 步骤 1: 校验图片
        ok, err = ImageUtils.validate(image_path)
        if not ok:
            print(f"❌ 图片校验失败: {err}")
            sys.exit(1)

        # 步骤 2: 计算 MD5
        md5_hash = ImageUtils.md5(image_path)
        print(f"📷 图片 MD5: {md5_hash}")

        # 步骤 3: 去重检查
        dup_record = self.index.find_by_md5(md5_hash)
        overwrite = False
        if dup_record is not None:
            print("")
            print("⚠️  这张试卷已经录入过了：")
            print(f"   - 科目：{dup_record.get('subject', '未知')} | "
                  f"年级：{dup_record.get('grade', '未知')}")
            print(f"   - 试卷：{dup_record.get('exam_name', '')}")
            print(f"   - 录入时间：{dup_record.get('created_at', '未知')}")
            print(f"   - 错题数：{dup_record.get('wrong_count', 0)} 道")
            print("")
            ans = input("是否需要重新录入（覆盖）？[y/N] ").strip().lower()
            if ans in ("y", "yes"):
                overwrite = True
            else:
                print("已取消。")
                return

        # 步骤 4: 保存图片
        ext = Path(image_path).suffix.lower()
        img_filename = f"{md5_hash}{ext}"
        img_abs = self.images_dir / img_filename
        ImageUtils.save(image_path, str(img_abs))
        img_rel = f"images/{img_filename}"
        print(f"✅ 图片已保存: {img_rel}")

        # 步骤 5: 调用 API
        print(f"🚀 正在提交批改任务...")
        try:
            job_id = submit_job(image_path, sid, skey)
            print(f"   任务已提交，JobId: {job_id}")
            print(f"⏳ 正在等待批改结果（最长 {API_MAX_WAIT} 秒）...", end="", flush=True)
            mark_infos = query_result(job_id, sid, skey, API_MAX_WAIT, API_POLL_INTERVAL)
            print(" 完成")
        except Exception as e:
            print(f"\n❌ API 调用失败: {e}")
            sys.exit(1)

        # 步骤 6: 解析错题
        wrong_items = parse_response(mark_infos)
        total_qs = sum(len(q.MarkInfos or []) for q in mark_infos)

        if not wrong_items:
            print("🎉 没有发现错题，太棒了！")
            return

        # 步骤 7: 推断元信息（如未提供）
        if not subject:
            subject = self._infer_subject(mark_infos, wrong_items)
        if not grade:
            grade = self._infer_grade(mark_infos, wrong_items)

        # 步骤 8: 生成 Markdown
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

        # 文件名
        file_name = f"错题库_{grade}{subject}"
        if exam_name:
            file_name += f"_{exam_name}"
        file_name += ".md"
        md_path = self.wab_dir / file_name
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # 步骤 9: 更新索引
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
            # 找到并更新已有记录
            for i, r in enumerate(self.index.records):
                if r.get("md5") == md5_hash:
                    self.index.update(i, record)
                    break
        else:
            self.index.add(record)

        # 步骤 10: 输出汇总
        print("")
        print(f"✅ 错题库已生成：wrong-answer-book/{file_name}")
        print("")
        print("📊 本次统计：")
        print(f"   - 试卷：{grade}{subject} {exam_name}")
        print(f"   - 错题：{len(wrong_items)} 道 / 共 {total_qs} 题")
        weak_kps = set()
        for item in wrong_items:
            for kp in item.get("knowledge_points", []):
                weak_kps.add(kp)
        if weak_kps:
            print(f"   - 薄弱点：{'、'.join(list(weak_kps)[:5])}")
        total_records = len(self.index.records)
        total_wrong = sum(r.get("wrong_count", 0) for r in self.index.records)
        total_mastered = sum(len(r.get("mastered", [])) for r in self.index.records)
        print("")
        print(f"📈 累计统计：已录入 {total_records} 份卷子，共 {total_wrong} 道错题"
              f"（{total_mastered} 道已掌握）")

    @staticmethod
    def _infer_subject(mark_infos, wrong_items) -> str:
        """从题目内容推断科目。"""
        all_text = ""
        for q in mark_infos:
            all_text += (q.MarkItemTitle or "") + " "
        for w in wrong_items:
            all_text += (w.get("handwrite", "") or "") + " "
        subjects = {"语文": ["语文", "拼音", "汉字", "词语", "阅读", "作文", "古诗"],
                    "数学": ["数学", "计算", "方程", "几何", "加减", "乘除", "面积"],
                    "英语": ["英语", "English", "单词", "语法", "阅读"],
                    "物理": ["物理", "力学", "电学", "光学"],
                    "化学": ["化学", "反应", "元素", "方程"]}
        for sub, keywords in subjects.items():
            if any(kw in all_text for kw in keywords):
                return sub
        return "未知"

    @staticmethod
    def _infer_grade(mark_infos, wrong_items) -> str:
        """从题目内容推断年级。"""
        all_text = ""
        for q in mark_infos:
            all_text += (q.MarkItemTitle or "") + " "
        for w in wrong_items:
            all_text += (w.get("handwrite", "") or "") + " "
        grades = {str(g): [str(g), f"{g}年级", f"{g}年"] for g in range(1, 13)}
        # 也匹配一年级、二年级...
        cn_grades = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六",
                     7: "七", 8: "八", 9: "九", 10: "十", 11: "十一", 12: "十二"}
        for num, cn in cn_grades.items():
            if f"{cn}年级" in all_text or f"小学{cn}年" in all_text or f"初中{cn}年" in all_text:
                return f"{num}年级"
        return "未知"

    # ── list ───────────────────────────────────────────────────────

    def cmd_list(self, tree: bool = True) -> None:
        """层级化列出所有错题记录。"""
        records = self.index.valid_records()
        if not records:
            print("📚 错题库为空，请先分析试卷。")
            return

        total_wrong = sum(r.get("wrong_count", 0) for _, r in records)
        total_mastered = sum(len(r.get("mastered", [])) for _, r in records)

        print(f"📚 错题库 | 共 {len(records)} 份卷子，{total_wrong} 道错题"
              f"（{total_mastered} 道已掌握）")
        print("")

        for idx, rec in records:
            mastered_count = len(rec.get("mastered", []))
            extra = f"（{mastered_count}题已掌握）" if mastered_count else ""
            date_str = rec.get("created_at", "")[:10] or "未知"
            print(f"[{idx + 1}] {rec.get('grade', '')}{rec.get('subject', '')}"
                  f" {rec.get('exam_name', '')}"
                  f" | {date_str}"
                  f" | {rec.get('wrong_count', 0)}错/{rec.get('total_questions', '?')}题"
                  f" {extra}")

            if tree:
                md_path = self.wab_dir / rec["file"]
                table_rows = MarkdownParser.extract_wrong_table(str(md_path))
                for row in table_rows:
                    seq = row["序号"]
                    is_mastered = seq in rec.get("mastered", [])
                    prefix = "✅ " if is_mastered else ""
                    suffix = " [已掌握]" if is_mastered else ""
                    display = f"{row['大题']} — {row['小题']}"
                    if len(display) > 40:
                        display = display[:37] + "..."
                    print(f"    ├─ {idx + 1}.{seq} {prefix}{display}{suffix}")
                print("")

    # ── view ───────────────────────────────────────────────────────

    def cmd_view(self, ref: str) -> None:
        """查看指定试卷或单题的完整详情。"""
        # 解析引用: "1" 或 "1.2"
        if "." in ref:
            rec_num, seq_str = ref.split(".", 1)
            rec_idx = int(rec_num) - 1
            seq = int(seq_str)
            single = True
        else:
            rec_idx = int(ref) - 1
            seq = 0
            single = False

        valid = self.index.valid_records()
        if rec_idx < 0 or rec_idx >= len(valid):
            print(f"❌ 无效编号: [{ref}]")
            return
        _, rec = valid[rec_idx]

        if single:
            md_path = self.wab_dir / rec["file"]
            details = MarkdownParser.extract_wrong_details(str(md_path), seq)
            if details is None:
                print(f"❌ 未找到错题 {ref}")
                return

            is_mastered = seq in rec.get("mastered", [])
            mastered_label = " ✅ 已掌握" if is_mastered else ""

            print(f"--- [{rec_idx + 1}] {rec.get('grade', '')}{rec.get('subject', '')}"
                  f" {rec.get('exam_name', '')}"
                  f" | {rec.get('wrong_count', 0)}错/{rec.get('total_questions', '?')}题 ---")
            print("")
            print(f"### {ref} — {details.get('大题', '')}{mastered_label}")
            print("")
            print(f"大题：{details.get('大题', '')}")
            if details.get("原题"):
                print(f"原题：{details.get('原题', '')}")
            print(f"答错空：{details.get('答错空', '')}")
            print("")
            print(f"| 我的答案 | {details.get('我的答案', '')} |")
            print(f"| 正确答案 | {details.get('正确答案', '')} |")
            print(f"| 错误原因 | {details.get('错误原因', '')} |")
        else:
            # 查看整份试卷
            md_path = self.wab_dir / rec["file"]
            with open(md_path, "r", encoding="utf-8") as f:
                print(f.read())

    # ── stats ──────────────────────────────────────────────────────

    def cmd_stats(self, subject: str = "", grade: str = "") -> None:
        """统计查询。"""
        records = self.index.records
        if not records:
            print("📊 暂无疑题记录。")
            return

        # 过滤
        filtered = records
        if subject:
            filtered = [r for r in filtered if subject in r.get("subject", "")]
        if grade:
            filtered = [r for r in filtered if grade in r.get("grade", "")]

        if not filtered:
            print(f"📊 未找到匹配的记录。")
            return

        total_wrong = sum(r.get("wrong_count", 0) for r in filtered)
        total_qs = sum(r.get("total_questions", 0) for r in filtered)
        total_mastered = sum(len(r.get("mastered", [])) for r in filtered)

        print("📊 错题统计")
        print("")
        print(f"   试卷数：{len(filtered)} 份")
        print(f"   总题数：{total_qs} 道")
        print(f"   错题数：{total_wrong} 道")
        print(f"   已掌握：{total_mastered} 道")
        if total_wrong > 0:
            print(f"   未掌握：{total_wrong - total_mastered} 道")
            print(f"   掌握率：{total_mastered / total_wrong * 100:.0f}%")

        # 按科目分组
        by_subject: dict[str, dict] = {}
        for r in filtered:
            sub = r.get("subject", "未知")
            if sub not in by_subject:
                by_subject[sub] = {"wrong": 0, "mastered": 0, "count": 0}
            by_subject[sub]["wrong"] += r.get("wrong_count", 0)
            by_subject[sub]["mastered"] += len(r.get("mastered", []))
            by_subject[sub]["count"] += 1

        if len(by_subject) > 1:
            print("")
            print("按科目：")
            for sub, data in sorted(by_subject.items()):
                print(f"   {sub}: {data['wrong']} 错（{data['mastered']} 已掌握）")

        # 按年级分组
        by_grade: dict[str, dict] = {}
        for r in filtered:
            gd = r.get("grade", "未知")
            if gd not in by_grade:
                by_grade[gd] = {"wrong": 0, "mastered": 0, "count": 0}
            by_grade[gd]["wrong"] += r.get("wrong_count", 0)
            by_grade[gd]["mastered"] += len(r.get("mastered", []))
            by_grade[gd]["count"] += 1

        if len(by_grade) > 1:
            print("")
            print("按年级：")
            for gd in sorted(by_grade.keys()):
                data = by_grade[gd]
                print(f"   {gd}: {data['wrong']} 错（{data['mastered']} 已掌握）")

    # ── master / unmaster ──────────────────────────────────────────

    def cmd_master(self, ref: str) -> None:
        """标记错题为已掌握。"""
        self._set_mastery(ref, True)

    def cmd_unmaster(self, ref: str) -> None:
        """取消错题的已掌握标记。"""
        self._set_mastery(ref, False)

    def _set_mastery(self, ref: str, mastered: bool) -> None:
        """统一处理掌握状态的标记/取消。"""
        if "." not in ref:
            print("❌ 请使用 N.M 格式指定单题，如: 1.2")
            return
        rec_num, seq_str = ref.split(".", 1)
        rec_idx = int(rec_num) - 1
        seq = int(seq_str)

        valid = self.index.valid_records()
        if rec_idx < 0 or rec_idx >= len(valid):
            print(f"❌ 无效编号: [{rec_num}]")
            return
        vi, rec = valid[rec_idx]
        # 用原始索引更新
        orig_idx = vi

        mastered_list = rec.get("mastered", [])

        if mastered:
            if seq in mastered_list:
                print(f"⚠️  错题 {ref} 已经是「已掌握」状态。")
                return
            mastered_list = sorted(mastered_list + [seq])
            MarkdownUpdater.update_mastery(
                str(self.wab_dir / rec["file"]), seq, True
            )
            print(f"✅ 已标记 [{rec_num}] 中错题 {ref} 为已掌握")
        else:
            if seq not in mastered_list:
                print(f"⚠️  错题 {ref} 尚未标记为已掌握。")
                return
            mastered_list = [s for s in mastered_list if s != seq]
            MarkdownUpdater.update_mastery(
                str(self.wab_dir / rec["file"]), seq, False
            )
            print(f"✅ 已取消 [{rec_num}] 中 {ref} 的已掌握标记")

        rec["mastered"] = mastered_list
        self.index.update(orig_idx, rec)

        wrong_count = rec.get("wrong_count", 0)
        mastered_count = len(mastered_list)
        if mastered_count >= wrong_count:
            print(f"📊 [{rec_num}] 全部错题已掌握！")
        else:
            print(f"📊 [{rec_num}] 进度：{mastered_count}/{wrong_count} 已掌握")

    # ── help ───────────────────────────────────────────────────────

    @staticmethod
    def cmd_help(parser: argparse.ArgumentParser, cmd: str = "") -> None:
        """
        显示帮助信息。
        不带参数：显示总览（所有子命令列表 + 示例）。
        带子命令名：显示该子命令的详细参数说明。
        """
        if cmd:
            subparsers_action = None
            for action in parser._actions:
                if isinstance(action, argparse._SubParsersAction):
                    subparsers_action = action
                    break
            if subparsers_action and cmd in subparsers_action.choices:
                subparsers_action.choices[cmd].print_help()
            else:
                print(f"❌ 未知子命令: {cmd}")
                print(f"   可用命令: {', '.join(subparsers_action.choices.keys()) if subparsers_action else ''}")
        else:
            parser.print_help()

    # ── delete ─────────────────────────────────────────────────────

    def cmd_delete(self, ref: str) -> None:
        """删除试卷或单题记录。"""
        if "." in ref:
            self._delete_single(ref)
        else:
            self._delete_exam(ref)

    def _delete_exam(self, ref: str) -> None:
        """删除整份试卷记录。"""
        rec_idx = int(ref) - 1
        valid = self.index.valid_records()
        if rec_idx < 0 or rec_idx >= len(valid):
            print(f"❌ 无效编号: [{ref}]")
            return
        vi, rec = valid[rec_idx]

        ans = input(f"确认删除 [{ref}] {rec.get('grade', '')}{rec.get('subject', '')}"
                    f" {rec.get('exam_name', '')}？[y/N] ").strip().lower()
        if ans not in ("y", "yes"):
            print("已取消。")
            return

        # 删除 md 文件
        md_path = self.wab_dir / rec["file"]
        if md_path.exists():
            md_path.unlink()
        # 删除图片
        img_path = self.wab_dir / rec["image"]
        if img_path.exists():
            img_path.unlink()
        # 删除索引
        self.index.remove(vi)
        print(f"✅ 已删除 [{ref}] 整份试卷记录")

    def _delete_single(self, ref: str) -> None:
        """删除单个错题。"""
        rec_num, seq_str = ref.split(".", 1)
        rec_idx = int(rec_num) - 1
        seq = int(seq_str)

        valid = self.index.valid_records()
        if rec_idx < 0 or rec_idx >= len(valid):
            print(f"❌ 无效编号: [{rec_num}]")
            return
        vi, rec = valid[rec_idx]

        md_path = self.wab_dir / rec["file"]
        try:
            new_count = MarkdownUpdater.remove_wrong_item(str(md_path), seq)
        except ValueError as e:
            print(f"❌ {e}")
            return

        # 更新索引
        rec["wrong_count"] = new_count
        mastered = [s for s in rec.get("mastered", []) if s != seq]
        # >= seq 的已掌握序号减 1
        mastered = [(s - 1 if s > seq else s) for s in mastered]
        rec["mastered"] = mastered
        self.index.update(vi, rec)

        print(f"✅ 已删除 [{rec_num}] 中的错题 {ref}")

        if new_count > 0:
            print(f"📊 [{rec_num}] 剩余 {new_count} 道错题")
        else:
            print(f"📊 [{rec_num}] 已无线错题，是否删除整份试卷记录？")
            ans = input("删除整份试卷？[y/N] ").strip().lower()
            if ans in ("y", "yes"):
                self._delete_exam(rec_num)


# ═══════════════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    """构建 CLI 参数解析器。"""
    parser = argparse.ArgumentParser(
        prog="wrong_answer_book.py",
        description="智能错题库 — 试卷图片分析、错题管理与统计",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python wrong_answer_book.py init
  python wrong_answer_book.py analyze ./试卷.jpg --subject 语文 --grade 三年级 --exam 期中测试
  python wrong_answer_book.py list
  python wrong_answer_book.py view 1
  python wrong_answer_book.py view 1.2
  python wrong_answer_book.py stats
  python wrong_answer_book.py stats --subject 语文
  python wrong_answer_book.py master 1.1
  python wrong_answer_book.py unmaster 1.1
  python wrong_answer_book.py delete 1
  python wrong_answer_book.py delete 1.2
        """,
    )

    parser.add_argument(
        "-d", "--work-dir",
        default=".",
        help="工作目录（默认当前目录）",
    )

    sub = parser.add_subparsers(dest="command", help="可用子命令")

    # init
    p_init = sub.add_parser("init", help="初始化工作目录")
    p_init.add_argument("--force", action="store_true", help="强制覆盖已有模板")

    # analyze
    p_analyze = sub.add_parser("analyze", help="分析试卷图片")
    p_analyze.add_argument("image", help="试卷图片路径")
    p_analyze.add_argument("--subject", default="", help="科目（如：语文、数学）")
    p_analyze.add_argument("--grade", default="", help="年级（如：三年级）")
    p_analyze.add_argument("--exam", default="", help="试卷名称（如：期中测试题）")

    # list
    p_list = sub.add_parser("list", help="列出所有错题")
    p_list.add_argument("--flat", action="store_true", help="简洁模式（不展开单题详情）")

    # view
    p_view = sub.add_parser("view", help="查看试卷或单题详情")
    p_view.add_argument("ref", help="编号，如 '1'（试卷）或 '1.2'（单题）")

    # stats
    p_stats = sub.add_parser("stats", help="统计查询")
    p_stats.add_argument("--subject", default="", help="按科目过滤")
    p_stats.add_argument("--grade", default="", help="按年级过滤")

    # master
    p_master = sub.add_parser("master", help="标记错题为已掌握")
    p_master.add_argument("ref", help="单题编号，如 '1.2'")

    # unmaster
    p_unmaster = sub.add_parser("unmaster", help="取消已掌握标记")
    p_unmaster.add_argument("ref", help="单题编号，如 '1.2'")

    # delete
    p_delete = sub.add_parser("delete", help="删除试卷或单题记录")
    p_delete.add_argument("ref", help="编号，如 '1'（试卷）或 '1.2'（单题）")

    # help
    p_help = sub.add_parser("help", help="显示帮助信息")
    p_help.add_argument("cmd", nargs="?", default="", help="子命令名称（如 init, analyze, list 等）")

    return parser


def main():
    """CLI 入口函数。"""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    wab = WrongAnswerBook(work_dir=args.work_dir)

    if args.command == "init":
        wab.cmd_init(force=getattr(args, "force", False))

    elif args.command == "analyze":
        wab.cmd_analyze(
            image_path=args.image,
            subject=args.subject,
            grade=args.grade,
            exam_name=args.exam,
        )

    elif args.command == "list":
        wab.cmd_list(tree=not args.flat)

    elif args.command == "view":
        wab.cmd_view(args.ref)

    elif args.command == "stats":
        wab.cmd_stats(subject=args.subject, grade=args.grade)

    elif args.command == "master":
        wab.cmd_master(args.ref)

    elif args.command == "unmaster":
        wab.cmd_unmaster(args.ref)

    elif args.command == "delete":
        wab.cmd_delete(args.ref)

    elif args.command == "help":
        wab.cmd_help(parser, args.cmd)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
