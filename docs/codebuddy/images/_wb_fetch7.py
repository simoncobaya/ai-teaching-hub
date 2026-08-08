import urllib.request
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

base = 'https://www.workbuddy.cn'

# Try fetching content pages directly - VitePress may serve raw markdown
pages = [
    '/docs/workbuddy/Overview',
    '/docs/workbuddy/Quickstart',
    '/docs/workbuddy/From-Beginner-to-Expert-Guide/Installation-Win-Guide',
    '/docs/workbuddy/From-Beginner-to-Expert-Guide/Installation-Mac-Guide',
]

for page in pages:
    url = base + page
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    # Find modulepreload links (these are the content chunks)
    preloads = re.findall(r'href=["\']([^"\']*\.lean\.js)["\']', html)
    chunks = re.findall(r'href=["\']([^"\']*\.js)["\']', html)
    
    # Filter for content chunks (usually contain page path hints)
    content_chunks = [c for c in chunks if 'md.' in c or 'lean' in c]
    
    print(f"\n=== {page} ===")
    print(f"Content chunks: {content_chunks}")
    
    # Also check for __VP_HASH__ or similar patterns
    vp_data = re.findall(r'__VP_\w+__', html)
    if vp_data:
        print(f"VP markers: {set(vp_data)}")

# Now try to construct content chunk URLs based on VitePress naming convention
# VitePress content chunks are typically at /docs/static/{page_path_with_underscores}.md.{hash}.js
# Let me try the metadata.js to find chunk mappings
with open('_wb_meta.js', 'r', encoding='utf-8') as f:
    meta = f.read()

# Search for the hash mapping pattern
# VitePress stores: "page_path" -> "hash" in a map
# The metadata typically contains the sidebar and some config
# Let me search for Installation-Win or Installation-Mac
win_section = re.findall(r'.{0,100}Installation-Win.{0,200}', meta)
print("\n=== Installation-Win in metadata ===")
for s in win_section:
    print(s)

mac_section = re.findall(r'.{0,100}Installation-Mac.{0,200}', meta)
print("\n=== Installation-Mac in metadata ===")
for s in mac_section:
    print(s)
