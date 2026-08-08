import urllib.request
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

base = 'https://www.workbuddy.cn'

# Read sidebar.js
with open('_wb_sidebar.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract WorkBuddy section from sidebar
wb_start = content.find('/workbuddy/Overview')
if wb_start > 0:
    # Get surrounding context
    start = max(0, wb_start - 200)
    end = min(len(content), wb_start + 2000)
    print("=== WorkBuddy sidebar section ===")
    print(content[start:end])

print("\n\n=== Full WorkBuddy-related links ===")
# Extract all links containing 'workbuddy'
links = re.findall(r'\{text:"([^"]+)",link:"(/workbuddy[^"]+)"\}', content)
for text, link in links:
    print(f"{text}: {link}")

# Also check for workbuddyapp and workbuddymini
links2 = re.findall(r'\{text:"([^"]+)",link:"(/workbuddy(?:app|mini)[^"]+)"\}', content)
print("\n=== WorkBuddy App/Mini links ===")
for text, link in links2:
    print(f"{text}: {link}")

# Now try to find the dynamic import map in theme.js
with open('_wb_theme.js', 'r', encoding='utf-8') as f:
    theme = f.read()

# Look for import() calls
imports = re.findall(r'import\((["\'][^"\']+\.js["\'])\)', theme)
print(f"\n=== Dynamic imports in theme.js ({len(set(imports))}) ===")
for i in sorted(set(imports)):
    print(i)

# Also search for the pattern VitePress uses: a map of routes to lazy imports
# It usually looks like: {path:()=>import(url)}
# Let me search more broadly
chunks = re.findall(r'["\']\.([.]?/[^"\']+\.js)["\']', theme)
print(f"\n=== Relative JS chunks ({len(set(chunks))}) ===")
for c in sorted(set(chunks)):
    if 'workbuddy' in c.lower() or 'install' in c.lower() or 'download' in c.lower() or 'beginner' in c.lower() or 'quick' in c.lower() or 'overview' in c.lower():
        print(c)
