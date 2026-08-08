import urllib.request
import re

base = 'https://www.workbuddy.cn'

# Fetch app.js to find route-to-chunk mapping
url = base + '/docs/static/app.BM8GR1d-.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
content = urllib.request.urlopen(req).read().decode('utf-8')

with open('_wb_app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"app.js length: {len(content)}")

# Find the chunk mapping - VitePress uses a dynamic import map
# Look for patterns like "Getting-Started_Download-and-Install" or route paths
install_refs = re.findall(r'[^\s"\'()]{0,50}(?:Getting-Started|Download|Install|Installation)[^\s"\'()]{0,80}', content)
print("\n=== Install-related refs ===")
for r in sorted(set(install_refs)):
    print(r)

# Also find all .lean.js references
lean_refs = re.findall(r'[\w/.-]+\.lean\.js', content)
print("\n=== Lean.js refs ===")
for l in sorted(set(lean_refs)):
    print(l)

# Find all md.js references (content chunks)
md_refs = re.findall(r'[\w/.-]+\.md\.[\w]+\.(?:js|lean\.js)', content)
print("\n=== md.js refs ===")
for m in sorted(set(md_refs)):
    print(m)

# Also fetch metadata.js
url2 = base + '/docs/static/chunks/metadata.8721b490.js'
req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
content2 = urllib.request.urlopen(req2).read().decode('utf-8')
with open('_wb_meta.js', 'w', encoding='utf-8') as f:
    f.write(content2)
print(f"\nmetadata.js length: {len(content2)}")

# Search for install/download in metadata
install_meta = re.findall(r'[^\s"\'()]{0,80}(?:Getting-Started|Download|Install|Installation|Overview)[^\s"\'()]{0,80}', content2)
print("\n=== Install refs in metadata ===")
for r in sorted(set(install_meta)):
    print(r)
