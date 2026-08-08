#!/usr/bin/env python3
"""
生成 CodeBuddy 和 WorkBuddy 的 PDF 文档。

使用 Microsoft Edge 无头模式渲染 HTML → PDF。
依赖: pip install markdown
用法: python gen-buddy-pdfs.py
"""

import os
import re
import sys
import base64
import subprocess
import markdown
from pathlib import Path

# ── 路径 ──────────────────────────────────────────────
BASE = Path(__file__).resolve().parent
DOCS = BASE / ".."  # docs/
OUT_DIR = BASE                      # teacher/

# ── Edge 路径 ─────────────────────────────────────────
EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

def find_edge() -> str:
    for p in EDGE_CANDIDATES:
        if os.path.exists(p):
            return p
    raise RuntimeError("未找到 Microsoft Edge，无法生成 PDF。")

# ── 通用 CSS ──────────────────────────────────────────
CSS = """
@page {
  size: A4;
  margin: 18mm 16mm;
}
body {
  font-family: "Microsoft YaHei", "Noto Sans CJK SC", "Segoe UI", sans-serif;
  font-size: 13px;
  line-height: 1.75;
  color: #333;
  max-width: 100%;
}
h1 {
  font-size: 26px;
  color: #1a5fb4;
  border-bottom: 3px solid #1a5fb4;
  padding-bottom: 8px;
  margin-top: 0;
  page-break-before: always;
}
h1:first-of-type { page-break-before: auto; }
h2 {
  font-size: 20px;
  color: #26a269;
  margin-top: 1.4em;
  page-break-after: avoid;
}
h3 { font-size: 16px; color: #444; page-break-after: avoid; }
h4 { font-size: 14px; color: #555; page-break-after: avoid; }
p { margin: 0.6em 0; }
pre {
  background: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 10px 14px;
  font-family: "Consolas", "Cascadia Code", monospace;
  font-size: 12px;
  line-height: 1.55;
  white-space: pre-wrap;
  word-break: break-all;
  page-break-inside: avoid;
}
code {
  font-family: "Consolas", "Cascadia Code", monospace;
  background: #f0f0f0;
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 12px;
}
pre code { background: none; padding: 0; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
  font-size: 12.5px;
}
th, td {
  border: 1px solid #d0d7de;
  padding: 6px 10px;
  text-align: left;
  vertical-align: top;
}
th { background: #eef4fb; font-weight: bold; }
blockquote {
  background: #f0f7ff;
  border-left: 4px solid #3584e4;
  margin: 10px 0;
  padding: 8px 14px;
  border-radius: 0 6px 6px 0;
  page-break-inside: avoid;
}
ul, ol { margin: 6px 0; padding-left: 1.6em; }
li { margin: 3px 0; }
strong { color: #1a1a1a; }
hr { border: none; border-top: 1px solid #ddd; margin: 18px 0; }
a { color: #1a5fb4; text-decoration: none; }
img { max-width: 100%; height: auto; }
"""


def embed_images(html: str, base_dir: Path) -> str:
    """将 HTML 中的相对路径图片转为 base64 data URI。"""
    def replacer(match):
        alt = match.group(1)
        src = match.group(2)
        if src.startswith("http"):
            return match.group(0)
        img_path = (base_dir / src).resolve()
        if not img_path.exists():
            return f'<img alt="{alt}" src="{src}" />'
        ext = img_path.suffix.lstrip(".").lower()
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "gif": "image/gif", "webp": "image/webp", "svg": "image/svg+xml"}.get(ext, "image/png")
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f'<img alt="{alt}" src="data:{mime};base64,{data}" />'

    return re.sub(r'<img[^>]*alt="([^"]*)"[^>]*src="([^"]+)"[^>]*/?\s*>', replacer, html)


def strip_nav_lines(md: str) -> str:
    """去掉页脚导航行"""
    return re.sub(r"^\[[⬅➡].*\]\(.*\)$", "", md, flags=re.MULTILINE)


def md_files_to_html(md_files: list[Path], title: str) -> str:
    """合并多个 Markdown 文件，转换为完整 HTML。"""
    combined = ""
    for mf in md_files:
        text = mf.read_text(encoding="utf-8")
        text = strip_nav_lines(text)
        combined += text + "\n\n"

    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
    body_html = md.convert(combined)

    base_dir = md_files[0].parent
    body_html = embed_images(body_html, base_dir)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{CSS}
</style>
</head>
<body>
{body_html}
</body>
</html>"""


def html_to_pdf(html_path: Path, pdf_path: Path, edge_exe: str):
    """用 Edge 无头模式将 HTML 转为 PDF。"""
    cmd = [
        edge_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={pdf_path}",
        "--print-to-pdf-no-header",
        str(html_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not pdf_path.exists():
        raise RuntimeError(f"PDF 生成失败: {result.stderr}")


def generate_pdf(name: str, md_files: list[Path], title: str, out_pdf: Path, edge_exe: str):
    """完整流程: MD → HTML → PDF"""
    print(f"  [{name}] 合并 {len(md_files)} 个 md 文件...")
    html = md_files_to_html(md_files, title)

    html_path = OUT_DIR / f"_tmp_{name}.html"
    html_path.write_text(html, encoding="utf-8")

    print(f"  [{name}] 生成 PDF → {out_pdf.name}")
    html_to_pdf(html_path, out_pdf, edge_exe)

    # 清理临时 HTML
    html_path.unlink()

    size_kb = out_pdf.stat().st_size / 1024
    print(f"  [{name}] 完成！({size_kb:.0f} KB)")


# ── 主流程 ────────────────────────────────────────────
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 55)
    print("  生成 CodeBuddy & WorkBuddy PDF 文档")
    print("=" * 55)

    edge_exe = find_edge()
    print(f"  Edge: {edge_exe}\n")

    # CodeBuddy
    cb_dir = DOCS / "codebuddy"
    generate_pdf(
        "CodeBuddy",
        [cb_dir / "README.md", cb_dir / "install.md", cb_dir / "versions.md"],
        "CodeBuddy（腾讯云代码助手）使用手册",
        OUT_DIR / "CodeBuddy-使用手册.pdf",
        edge_exe,
    )

    print()

    # WorkBuddy
    wb_dir = DOCS / "workbuddy"
    generate_pdf(
        "WorkBuddy",
        [wb_dir / "README.md", wb_dir / "install.md", wb_dir / "versions.md"],
        "WorkBuddy（腾讯 AI 办公助手）使用手册",
        OUT_DIR / "WorkBuddy-使用手册.pdf",
        edge_exe,
    )

    print("\n  全部完成！")
