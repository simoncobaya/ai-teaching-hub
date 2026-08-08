import urllib.request
import re

base = 'https://www.workbuddy.cn'

# Fetch theme.js which might have the route-to-chunk mapping
url = base + '/docs/static/chunks/theme.DoNf6NVW.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
content = urllib.request.urlopen(req).read().decode('utf-8')
print(f"theme.js length: {len(content)}")

# Save for inspection
with open('_wb_theme.js', 'w', encoding='utf-8') as f:
    f.write(content)

# Search for import patterns with any quotes
import_patterns = re.findall(r'["\'](/[^"\']*?)["\'][,)\s]*\([^)]*import[^)]*["\']([^"\']+\.js)["\']', content)
print(f"Route->chunk mappings: {len(import_patterns)}")

# Try simpler: find all .js file references
all_js = sorted(set(re.findall(r'[\w/./-]+\.js', content)))
workbuddy_js = [j for j in all_js if 'workbuddy' in j.lower() or 'install' in j.lower() or 'download' in j.lower() or 'beginner' in j.lower() or 'getting' in j.lower()]
print(f"\n=== WorkBuddy-related JS refs ({len(workbuddy_js)}) ===")
for j in workbuddy_js:
    print(j)

# Also check sidebar.js
url2 = base + '/docs/static/chunks/sidebar.bPOPvPLd.js'
req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
content2 = urllib.request.urlopen(req2).read().decode('utf-8')
print(f"\nsidebar.js length: {len(content2)}")
with open('_wb_sidebar.js', 'w', encoding='utf-8') as f:
    f.write(content2)

# Search for workbuddy/install/download in sidebar
wb_sidebar = re.findall(r'.{0,50}(?:workbuddy|Install|Download|Beginner).{0,50}', content2)
print(f"\n=== Sidebar matches ({len(wb_sidebar)}) ===")
for m in wb_sidebar[:20]:
    print(m)
