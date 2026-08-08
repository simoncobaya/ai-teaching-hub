import urllib.request
import re

# Fetch the CN docs installation page
url = 'https://www.workbuddy.cn/docs/workbuddy/Getting-Started/Download-and-Install'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Find JS asset files
js_files = sorted(set(re.findall(r'(/assets/[^"\']+\.js)', html)))
print("=== JS Assets ===")
for f in js_files:
    print(f)

# Find lean.js files (content chunks)
lean = [f for f in js_files if 'lean' in f]
print("\n=== Lean chunks ===")
for c in lean:
    print(c)
