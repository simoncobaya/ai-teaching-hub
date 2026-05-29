# 腾讯云 SubmitQuestionMarkAgentJob API 接口规范

> 本文档描述调用腾讯云 OCR「试题批改Agent」异步接口的完整规范。
> 实际调用脚本见 `scripts/submit_question_mark.py`。

---

## 接口概述

| 项目 | 说明 |
|------|------|
| 产品 | 文字识别 OCR |
| 提交接口 | `SubmitQuestionMarkAgentJob` |
| 查询接口 | `DescribeQuestionMarkAgentJob` |
| API 版本 | `2018-11-19` |
| 请求域名 | `ocr.tencentcloudapi.com` |
| 调用方式 | 异步（提交 → 轮询查询） |
| 并发限制 | 10张/分钟 |

---

## 一、SubmitQuestionMarkAgentJob（提交任务）

### 请求参数

| 参数名 | 必选 | 类型 | 描述 |
|--------|:---:|------|------|
| ImageBase64 | 否* | String | 图片/PDF Base64，不超过10M，分辨率建议600*800以上，支持PNG/JPG/JPEG/BMP/PDF |
| ImageUrl | 否* | String | 图片/PDF URL，图片下载时间不超过3秒，推荐存储于腾讯云COS |
| PdfPageNumber | 否 | Integer | PDF页面对应页码，默认值为1，仅支持单页识别 |
| QuestionConfigMap | 否 | String | 题目信息输出配置。`{"KnowledgePoints":true}` 输出知识点；`{"TrueAnswer":true}` 输出正确答案；`{"StepCorrection":true}` 启用步骤级批改 |
| ReferenceAnswer | 否 | String | 仅单题有效，作为参考答案输入批改模型 |
| ImageBase64List.N | 否 | Array of String | 图片Base64列表，最多三张。优先级高于单张 ImageBase64/ImageUrl |
| ImageUrlList.N | 否 | Array of String | 图片URL列表，最多三张。优先级：ImageUrlList > ImageBase64List > ImageBase64/ImageUrl |

> \* `ImageBase64` 和 `ImageUrl` 必须提供一个。推荐使用 `ImageBase64`。

### 响应参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| JobId | String | 任务唯一ID，由服务端生成 |
| QuestionInfo | Array of QuestionInfo | 切题边框坐标列表 |
| QuestionCount | String | 切题数量（计费依据） |
| RequestId | String | 唯一请求ID |

---

## 二、DescribeQuestionMarkAgentJob（查询任务结果）

### 请求参数

| 参数名 | 必选 | 类型 | 描述 |
|--------|:---:|------|------|
| JobId | 否 | String | 任务唯一ID |

### 响应参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| JobStatus | String | 任务状态：`WAIT`（等待中）/ `RUN`（执行中）/ `FAIL`（失败）/ `DONE`（成功） |
| ErrorCode | String | 任务执行错误码，不为FAIL时为空 |
| ErrorMessage | String | 任务执行错误信息，不为FAIL时为空 |
| Angle | Float | 图片旋转角度（度数），0为水平，顺时针为正 |
| MarkInfos | Array of MarkInfo | **试题批改信息（核心数据）** |
| RequestId | String | 唯一请求ID |

### MarkInfo 结构（核心批改数据）

MarkInfos 是嵌套的三级结构：**大题** → **小题** → **答案详情**

```
MarkInfos[                    # 大题列表
  {
    MarkItemTitle: "..."      # 大题题干
    AnswerInfos: []           # 大题级答案（通常为空）
    MarkInfos: [              # 该大题下的小题列表
      {
        MarkItemTitle: "..."  # 小题题干（如 "(1)小琪猜测..."）
        AnswerInfos: [        # 该小题的答案详情列表
          {
            AnswerAnalysis: "..."      # 详细答案解析
            HandwriteInfo: "..."       # 学生手写作答内容（LaTeX格式）
            HandwriteInfoPositions: []  # 手写坐标 [x1,y1,x2,y2,x3,y3,x4,y4]
            IsCorrect: true/false      # 作答是否正确
            KnowledgePoints: []        # 知识点列表（需 QuestionConfigMap 开启）
            RightAnswer: ""            # 正确答案（需 QuestionConfigMap 开启）
          }
        ]
      }
    ]
  }
]
```

### 错题判定规则

- **遍历 MarkInfos** → 对每道小题的 `AnswerInfos`，检查 `IsCorrect`
- `IsCorrect == false` → 记录为错题
- 从 `AnswerAnalysis` 提取错误原因
- 从 `KnowledgePoints` 提取薄弱知识点
- 从 `HandwriteInfo` 提取学生作答内容
- 从 `RightAnswer` 获取正确答案

---

## 三、调用方式

直接执行脚本，传入图片路径即可：

```bash
# 安装依赖（一次性）
pip install tencentcloud-sdk-python

# 执行脚本，输出 JSON 到 stdout
python scripts/submit_question_mark.py wrong-answer-book/images/{MD5}.{ext}
```

脚本内部流程：
1. 从 `credentials.md` 加载 SecretId/SecretKey
2. 对图片做 Base64 编码
3. 调用 `SubmitQuestionMarkAgentJob` 提交任务（`QuestionConfigMap` 已开启 KnowledgePoints + TrueAnswer + StepCorrection）
4. 每 3 秒轮询 `DescribeQuestionMarkAgentJob`，最长等待 120 秒
5. 解析 MarkInfos，筛选 `IsCorrect==false` 的错题
6. 输出 JSON 到 stdout（含 `wrong_count` / `wrong_items`），进度信息输出到 stderr

---

## 四、错误码（DescribeQuestionMarkAgentJob）

| 错误码 | 描述 |
|--------|------|
| FailedOperation.DownLoadError | 文件下载失败 |
| FailedOperation.ImageDecodeFailed | 图片解码失败 |
| FailedOperation.ImageSizeTooLarge | 图片尺寸过大 |
| FailedOperation.OcrFailed | OCR识别失败 |
| FailedOperation.PDFParseFailed | PDF解析失败 |
| FailedOperation.UnKnowError | 未知错误 |
| FailedOperation.UnKnowFileTypeError | 未知文件类型 |
| FailedOperation.UnOpenError | 服务未开通 |
| LimitExceeded.TooLargeFileError | 文件内容太大 |
| ResourceUnavailable.InArrears | 账号已欠费 |
| ResourceUnavailable.ResourcePackageRunOut | 资源包耗尽 |

---

## 五、Skill 中的调用流程

在 SKILL.md 的阶段2中，按以下步骤调用：

1. **读取认证**：从项目根目录的 `credentials.md` 解析 SecretId / SecretKey
2. **Base64 编码**：读取 `wrong-answer-book/images/{MD5}.{ext}` 进行 Base64 编码
3. **提交任务**：调用 `SubmitQuestionMarkAgentJob`，设置 `QuestionConfigMap={"KnowledgePoints":true,"TrueAnswer":true,"StepCorrection":true}`
4. **轮询等待**：每3秒调用 `DescribeQuestionMarkAgentJob`，最长等待120秒
5. **解析结果**：遍历 `MarkInfos` → `MarkInfos[].MarkInfos[].AnswerInfos`，筛选 `IsCorrect==false` 的错题
6. **输出 JSON**：将错题列表输出为 JSON，传给阶段3进行错题库写入
