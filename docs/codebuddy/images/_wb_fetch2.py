import urllib.request
import re

# Fetch the CN docs installation page
url = 'https://www.workbuddy.cn/docs/workbuddy/Getting-Started/Download-and-Install'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Save raw HTML for inspection
with open('_wb_page.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"HTML length: {len(html)}")

# Find all script src
scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html)
print("\n=== Script srcs ===")
for s in scripts:
    print(s)

# Find all link href
links = re.findall(r'<link[^>]*href=["\']([^"\']+)["\']', html)
print("\n=== Link hrefs ===")
for l in links:
    print(l)

# Find modulepreload
preloads = re.findall(r'modulepreload[^>]*href=["\']([^"\']+)["\']', html)
print("\n=== Module preloads ===")
for p in preloads:
    print(p)

# Find any asset paths
assets = re.findall(r'["\'](/[^"\']*\.(?:js|css|json))["\']', html)
print("\n=== Asset paths ===")
for a in sorted(set(assets)):
    print(a)

# Find static paths  
statics = re.findall(r'["\']([^"\']*static[^"\']*)["\']', html)
print("\n=== Static paths ===")
for s in sorted(set(statics)):
    print(s)
