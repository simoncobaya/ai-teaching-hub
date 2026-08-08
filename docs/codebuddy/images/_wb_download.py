import urllib.request
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

base = 'https://www.workbuddy.cn'
out = 'd:/ai-teaching-hub/docs/workbuddy/images'

# Create output directory
os.makedirs(out, exist_ok=True)

images = {
    # Quickstart
    '/docs/static/quickstart-1.DGnw1yR0.png': 'quickstart-ui.png',
    
    # Windows install guide
    '/docs/static/image.nuc5Wzyg.png': 'win-download.png',
    '/docs/static/image-1.Cv_fWdeI.png': 'win-install-1.png',
    '/docs/static/image-2.nX8V0i5W.png': 'win-install-2-license.png',
    '/docs/static/image-3.C1dI3tJz.png': 'win-install-3-path.png',
    '/docs/static/image-4.B1FHUmlf.png': 'win-install-4-startmenu.png',
    '/docs/static/image-5.BlN7t4Co.png': 'win-install-5-shortcut.png',
    '/docs/static/image-6.BqsUqnLs.png': 'win-install-6-confirm.png',
    '/docs/static/image-7.O4VQi_-H.png': 'win-install-7-complete.png',
    '/docs/static/image-8.CK0afJ4M.png': 'win-login-1-button.png',
    '/docs/static/image-9.B-sCZ4xM.png': 'win-login-2-wechat-qr.png',
    '/docs/static/image-10.Cyf1orgE.png': 'win-login-3-success.png',
    '/docs/static/image-11.DhncBaQi.png': 'win-update.png',
    '/docs/static/image-12.BL3Xs7uq.png': 'win-update-latest.png',
    
    # Mac install guide
    '/docs/static/image-13.BpXsVrXL.png': 'mac-download.png',
    '/docs/static/image-24.-gKY3-lT.png': 'mac-system-version.png',
    '/docs/static/image-14.BhZn1kDP.png': 'mac-download-browser.png',
    '/docs/static/image-15.sG7k4Kcf.png': 'mac-install-1-dmg.png',
    '/docs/static/image-16.2oor8hng.png': 'mac-install-2-drag.png',
    '/docs/static/image-17.BxSolkQv.png': 'mac-install-3-drag2.png',
    '/docs/static/image-18.B8WzN7p9.png': 'mac-install-4-copying.png',
    '/docs/static/image-19.BnT816LK.png': 'mac-install-5-eject.png',
    '/docs/static/image-20.CSF6dln-.png': 'mac-login-1-button.png',
    '/docs/static/image-21.BEKABQ55.png': 'mac-login-2-wechat-qr.png',
    '/docs/static/image-22.Da1Lz-Ry.png': 'mac-login-3-success.png',
    '/docs/static/image-23.C3iiE_yZ.png': 'mac-update.png',
}

for src, dst in images.items():
    url = base + src
    path = os.path.join(out, dst)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req).read()
        with open(path, 'wb') as f:
            f.write(data)
        print(f'OK: {dst} ({len(data)//1024} KB)')
    except Exception as e:
        print(f'FAIL: {dst} - {e}')
