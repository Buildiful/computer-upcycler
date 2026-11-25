"""Run with Python + Playwright and installed Chromium. No network downloads."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright
import os
ROOT=Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
def inline(name):
    html=(ROOT/name).read_text()
    import re, base64
    html=re.sub(r'<link rel="stylesheet" href="([^"]+)">',lambda m:'<style>'+(ROOT/m[1]).read_text()+'</style>',html)
    # Inline resources to support sandboxed browsers that block local HTTP navigation.
    scripts=[]
    def script(m):
        scripts.append('<script'+m[2].replace(' defer','')+'>'+(ROOT/m[1]).read_text()+'</script>')
        return ''
    html=re.sub(r'<script(?: defer)? src="([^"]+)"([^>]*)></script>',script,html)
    html=html.replace('</body>',''.join(scripts)+'</body>')
    html=html.replace('./assets/buildiful-logo-white.png','data:image/png;base64,'+base64.b64encode((ROOT/'assets/buildiful-logo-white.png').read_bytes()).decode())
    return html
with sync_playwright() as p, TemporaryDirectory() as tmp:
    browser=p.chromium.launch(executable_path=os.getenv('CHROMIUM','/usr/bin/chromium'),args=['--no-sandbox'])
    page=browser.new_page(accept_downloads=True,viewport={'width':390,'height':844})
    errors=[]; page.on('pageerror',lambda e:errors.append(str(e)))
    def start(osname,cpu='x64',goal='try'):
        global page
        page.close();page=browser.new_page(accept_downloads=True,viewport={'width':390,'height':844});page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(inline('index.html')); page.locator('#start').click();page.locator('#os').select_option(osname);page.locator('#cpu').select_option(cpu);page.locator('#goal').select_option(goal)
    def advance():
        page.locator('#next').click()
        for ident in ['backup','usb','requirements']:page.locator('#'+ident).check()
        page.locator('#next').click();page.locator('#ready').check();page.locator('#next').click()
    start('mac','arm');assert page.locator('#next').is_disabled();assert 'Apple Silicon' in page.locator('#gate').inner_text()
    start('mac');assert page.locator('#next').is_disabled();page.locator('#mac').select_option('no-t2');assert page.locator('#next').is_enabled();page.locator('#goal').select_option('dual');assert page.locator('#next').is_disabled()
    start('windows','x64','dual');assert page.locator('#next').is_disabled();page.locator('#encryption').select_option('off');assert page.locator('#next').is_enabled();advance();assert 'alongside' in page.locator('.guide').inner_text();assert 'Never choose Erase disk' in page.locator('.guide').inner_text();
    for fmt in ('png','pdf'):
        with page.expect_download() as d:page.locator('#'+fmt).click()
        path=Path(tmp)/('dual.'+fmt);d.value.save_as(path);assert path.read_bytes().startswith(b'%PDF' if fmt=='pdf' else b'\x89PNG');
        if os.getenv('EXPORT_TEST_DIR'):Path(os.environ['EXPORT_TEST_DIR'],path.name).write_bytes(path.read_bytes())
    start('linux','x64','try');advance();assert 'Try it without installing' in page.locator('.guide').inner_text();assert 'Replace your existing OS' not in page.locator('.guide').inner_text()
    start('windows','x64','replace');advance();assert 'permanently deletes' in page.locator('.guide').inner_text();assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    if os.getenv('EXPORT_TEST_DIR'):page.screenshot(path=str(Path(os.environ['EXPORT_TEST_DIR'])/'mobile.png'),full_page=True)
    page.close();page=browser.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.set_content(inline('privacy.html'));assert page.title().startswith('Privacy | Computer Upcycler');assert page.evaluate('window.BuildifulAnalytics.version')=='2.1.0';assert page.locator('#analyticsManageWrap').is_hidden();assert not errors,errors
    browser.close()
print('PASS: blocked hardware, Windows dual boot, Linux live trial, Windows replace, PNG/PDF downloads, mobile width, privacy page, no browser errors')
server.shutdown()
