import urllib.request
import re

base = 'https://www.workbuddy.cn'

# Fetch framework.js to find dynamic import map
url = base + '/docs/static/chunks/framework.BimBai0p.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
content = urllib.request.urlopen(req).read().decode('utf-8')
print(f"framework.js length: {len(content)}")

# Find all .js references that look like content chunks
js_refs = re.findall(r'"([\w/.-]+\.js)"', content)
print(f"\nTotal JS refs: {len(set(js_refs))}")

# Filter for md-related chunks
md_chunks = [r for r in js_refs if '.md.' in r]
print(f"\n=== MD chunks ({len(set(md_chunks))}) ===")
for m in sorted(set(md_chunks)):
    print(m)

# Also look for the import map pattern
# VitePress uses something like: {"/path/to/page":()=>import("./chunk.js")}
import_pattern = re.findall(r'"(/workbuddy[^"]*)"\s*:\s*[^}]*?"([^"]+\.js)"', content)
print(f"\n=== WorkBuddy route->chunk mapping ===")
for route, chunk in import_pattern:
    print(f"{route} -> {chunk}")

# Broader search
import_pattern2 = re.findall(r'"(/[^\"]*?)["\']\s*[,)]\s*\(\)\s*=>\s*import\(["\']([^"\']+\.js)["\']\)', content)
print(f"\n=== All route->chunk mappings ({len(import_pattern2)}) ===")
for route, chunk in import_pattern2[:30]:
    if 'workbuddy' in route.lower() or 'install' in route.lower() or 'download' in route.lower():
        print(f"{route} -> {chunk}")
