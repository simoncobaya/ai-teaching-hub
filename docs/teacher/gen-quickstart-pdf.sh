#!/bin/bash
# 重新生成 DeepSeek-Claude-Code-快速入门.pdf
# 内容源: docs/deepseek-claudecode/（README + 01~09）
# 依赖: pandoc, weasyprint (pip install weasyprint)
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS="$DIR/../deepseek-claudecode"
OUT="$DIR/DeepSeek-Claude-Code-快速入门.pdf"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

FILES=(README.md 01-deepseek.md 02-nodejs.md 03-claude-code.md 04-config.md \
       05-basics.md 06-verify.md 07-whack-a-mole.md 08-game-feel.md 09-troubleshooting.md)

# 1. 合并 md，去掉页脚导航行（[⬅️ 上一页…] / [➡️ 下一页…]）
for f in "${FILES[@]}"; do
  sed -E '/^\[[⬅➡].*\]\(.*\)$/d' "$DOCS/$f" >> "$TMP/all.md"
  echo "" >> "$TMP/all.md"
done

# 2. pandoc: markdown → HTML
# --standalone 生成完整 HTML（含 <meta charset="utf-8">），
# 否则 WeasyPrint 会用错误编码读文件导致中文乱码
pandoc "$TMP/all.md" -f markdown -t html5 --standalone \
  --metadata title="DeepSeek + Claude Code 快速入门" -o "$TMP/out.html"

# 3. weasyprint: HTML → PDF
python3 - <<EOF
import weasyprint
weasyprint.HTML("$TMP/out.html").write_pdf("$OUT", stylesheets=["$DIR/quickstart-pdf.css"])
EOF

echo "✅ 已生成: $OUT"
