import urllib.request
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

base = 'https://www.workbuddy.cn'

pages = {
    'overview': '/docs/static/workbuddy_Overview.md.Bu8Oag-v.js',
    'quickstart': '/docs/static/workbuddy_Quickstart.md.DhnaRlI2.js',
    'install-win': '/docs/static/workbuddy_From-Beginner-to-Expert-Guide_Installation-Win-Guide.md.HtDAKAgH.js',
    'install-mac': '/docs/static/workbuddy_From-Beginner-to-Expert-Guide_Installation-Mac-Guide.md.6DUEX-tr.js',
}

for name, path in pages.items():
    url = base + path
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    content = urllib.request.urlopen(req).read().decode('utf-8')
    
    with open(f'_wb_{name}.js', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n=== {name} (length: {len(content)}) ===")
    
    # Extract image URLs
    img_urls = sorted(set(re.findall(r'https?://[^\s"\'<>)\\]+\.(?:png|jpg|jpeg|gif|webp|svg)', content)))
    rel_imgs = sorted(set(re.findall(r'["\']([^"\']+\.(?:png|jpg|jpeg|gif|webp))["\']', content)))
    
    print(f"Absolute images: {len(img_urls)}")
    for u in img_urls:
        print(f"  {u}")
    print(f"Relative images: {len(rel_imgs)}")
    for u in rel_imgs:
        print(f"  {u}")
