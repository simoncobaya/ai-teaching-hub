#!/usr/bin/env python3
"""
submit_question_mark.py - 腾讯云试题批改Agent SDK调用脚本

调用腾讯云 OCR SubmitQuestionMarkAgentJob API 对试卷图片进行识别和批改，
提取错题列表并输出为 JSON，供错题库 Skill 使用。

运行方式:
    python submit_question_mark.py <图片路径> [credentials.md路径]

输出:
    JSON 到 stdout，包含 job_id / total_sub_questions / wrong_count / wrong_items
    进度信息输出到 stderr
"""

import sys
import json
import base64
import time
import re

from tencentcloud.common import credential
from tencentcloud.ocr.v20181119 import ocr_client, models
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException


def load_credentials(cred_file):
    """从 credentials.md 加载 SecretId/SecretKey"""
    with open(cred_file, "r", encoding="utf-8") as f:
        content = f.read()
    # 兼容有无反引号两种格式
    sid = re.search(r"SecretId\s*\|\s*`?([^`|\n]+?)`?\s*\|", content).group(1).strip()
    skey = re.search(r"SecretKey\s*\|\s*`?([^`|\n]+?)`?\s*\|", content).group(1).strip()
    return sid, skey


def submit_job(image_path, secret_id, secret_key):
    """
    提交试卷批改任务
    params:
        image_path - 本地图片文件路径
    returns:
        JobId (str)
    """
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")

    cred = credential.Credential(secret_id, secret_key)
    client = ocr_client.OcrClient(cred, "ap-guangzhou")

    req = models.SubmitQuestionMarkAgentJobRequest()
    req.ImageBase64 = img_base64
    # 开启知识点、正确答案和步骤级批改输出
    req.QuestionConfigMap = '{"KnowledgePoints":true,"TrueAnswer":true,"StepCorrection":true}'

    resp = client.SubmitQuestionMarkAgentJob(req)
    return resp.JobId


def query_result(job_id, secret_id, secret_key, max_wait=120, interval=3):
    """
    轮询查询异步任务结果
    params:
        job_id    - 任务ID
        max_wait  - 最大等待时间（秒），默认 120
        interval  - 轮询间隔（秒），默认 3
    returns:
        MarkInfos (list) — 批改信息列表
    """
    cred = credential.Credential(secret_id, secret_key)
    client = ocr_client.OcrClient(cred, "ap-guangzhou")

    req = models.DescribeQuestionMarkAgentJobRequest()
    req.JobId = job_id

    elapsed = 0
    while elapsed < max_wait:
        resp = client.DescribeQuestionMarkAgentJob(req)
        status = resp.JobStatus

        if status == "DONE":
            mark_infos = resp.MarkInfos or []
            return mark_infos
        elif status == "FAIL":
            raise RuntimeError(
                f"任务失败 [{resp.ErrorCode}]: {resp.ErrorMessage}"
            )

        time.sleep(interval)
        elapsed += interval

    raise TimeoutError(f"任务超时（{max_wait}秒内未完成）")


def parse_response(mark_infos):
    """
    解析 MarkInfos，提取错题列表
    returns:
        list[dict] — 错题信息，每项包含：
            big_question, sub_question, handwrite,
            analysis, right_answer, knowledge_points, is_correct
    """
    wrong_items = []
    for big_q in mark_infos:
        big_title = big_q.MarkItemTitle or ""
        for sub_q in (big_q.MarkInfos or []):
            sub_title = sub_q.MarkItemTitle or ""
            for ans in (sub_q.AnswerInfos or []):
                if not ans.IsCorrect:
                    wrong_items.append({
                        "big_question": big_title,
                        "sub_question": sub_title,
                        "handwrite": ans.HandwriteInfo or "",
                        "analysis": ans.AnswerAnalysis or "",
                        "right_answer": ans.RightAnswer or "",
                        "knowledge_points": list(ans.KnowledgePoints or []),
                        "is_correct": ans.IsCorrect,
                    })
    return wrong_items


def main(image_path, cred_file="credentials.md"):
    """
    完整调用流程，将结果输出为 JSON（stdout），进度信息输出到 stderr
    """
    sid, skey = load_credentials(cred_file)

    job_id = submit_job(image_path, sid, skey)
    print(f"任务已提交，JobId: {job_id}", file=sys.stderr)

    mark_infos = query_result(job_id, sid, skey)

    wrong_items = parse_response(mark_infos)

    result = {
        "job_id": job_id,
        "total_sub_questions": sum(
            len(q.MarkInfos or []) for q in mark_infos
        ),
        "wrong_count": len(wrong_items),
        "wrong_items": wrong_items,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python submit_question_mark.py <图片路径> [credentials.md路径]", file=sys.stderr)
        sys.exit(1)
    image_path = sys.argv[1]
    cred_file = sys.argv[2] if len(sys.argv) > 2 else "credentials.md"
    main(image_path, cred_file)
