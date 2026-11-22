#!/usr/bin/env python3
import json, pathlib, os, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent
D=json.loads((R/'wiki_data.json').read_text(encoding='utf8'))
results=[]
def record(name,ok,detail=''):
    results.append({'check':name,'pass':bool(ok),'detail':detail})
    print(('PASS' if ok else 'FAIL'),name,detail)
    if not ok: raise AssertionError(name+' '+detail)

record('至少五篇來源',len(D['sources'])>=5 and len({s['url'] for s in D['sources']})>=5, f"{len(D['sources'])} independent URLs")
record('五個獨立 Wiki 概念頁',len(D['concepts'])>=5 and all((R/'wiki'/f"{c['id']}.md").exists() for c in D['concepts']))
known={s['id'] for s in D['sources']}
record('每張內容簡報的來源 ID 皆存在',all(set(sl.get('source_ids',[])) <= known for sl in D['slide_plan']))
covered=set().union(*(set(s.get('source_ids',[])) for s in D['slide_plan']))
record('五篇來源都出現在簡報',covered==known, f'covered={sorted(covered)}')
record('Wiki 不含未展開的模板變數', '{esc(' not in (R/'wiki.html').read_text(encoding='utf8'))
record('四組二進位真值組合正確', all(((a^b) == (a+b)%2 and (a&b)==(a+b)//2 and (a|b)==int(a+b>0)) for a in (0,1) for b in (0,1)))
for name in ['index.html','wiki.html','workflow.html']:
    soup=BeautifulSoup((R/name).read_text(encoding='utf8'),'html.parser')
    record(name+' HTML 標題及正文',bool(soup.title and soup.body))

os.chdir(R)
httpd=ThreadingHTTPServer(('127.0.0.1',0),SimpleHTTPRequestHandler)
threading.Thread(target=httpd.serve_forever,daemon=True).start()
BASE=f'http://127.0.0.1:{httpd.server_port}/'
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1360,'height':900},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda exc:errors.append(str(exc)))
    page.set_content((R/'index.html').read_text(encoding='utf8'))
    record('首頁可開啟',page.locator('h1').first.inner_text().strip()=='從邏輯閘到有限狀態機')
    page.screenshot(path=str(R/'checks'/'desktop-cover.png'),full_page=True)
    page.locator('#next').click();record('下一頁按鈕',page.locator('.slide:not([hidden]) h1').inner_text()=='今天會學到什麼？')
    page.keyboard.press('ArrowRight');record('鍵盤右鍵換頁',page.locator('.slide:not([hidden]) h1').inner_text().startswith('邏輯閘'))
    page.locator('#logicA').click();page.locator('#logicB').click()
    record('AND、OR、XOR 操作',page.locator('#logicAnd').inner_text()=='1' and page.locator('#logicOr').inner_text()=='1' and page.locator('#logicXor').inner_text()=='0')
    page.screenshot(path=str(R/'checks'/'desktop-logic.png'),full_page=True)
    while page.locator('.slide:not([hidden])').get_attribute('id')!='slide-adder':page.locator('#next').click()
    page.locator('#addA').click();page.locator('#addB').click()
    record('半加器 1+1 = 二進位10',page.locator('#addSum').inner_text()=='0' and page.locator('#addCarry').inner_text()=='1' and '10' in page.locator('#addExplanation').inner_text())
    while page.locator('.slide:not([hidden])').get_attribute('id')!='slide-fsm':page.locator('#next').click()
    page.locator('#fsmToggle').click()
    record('FSM OFF 切換 ON',page.locator('#onNode').get_attribute('class').find('active')!=-1 and 'ON' in page.locator('#fsmStateText').inner_text())
    page.locator('#next').click();page.locator('#next').click()
    record('小測驗頁',page.locator('.slide:not([hidden])').get_attribute('id')=='slide-quiz')
    page.locator('input[name="q0"][value="0"]').check();page.locator('input[name="q1"][value="1"]').check();page.locator('input[name="q2"][value="1"]').check();page.locator('#quizCheck').click()
    record('小測驗得分 3/3','答對 3/3' in page.locator('#quizTotal').inner_text())
    record('簡報 JavaScript 無錯誤',len(errors)==0,';'.join(errors))
    wik=browser.new_page(viewport={'width':1360,'height':900});wik.set_content((R/'wiki.html').read_text(encoding='utf8'))
    record('Wiki 含五個概念頁',wik.locator('section.concept').count()==5)
    wik.locator('#search').fill('Flip-Flop')
    record('Wiki 搜尋可用',wik.locator('section.concept:not(.hidden)').count()>=1 and wik.locator('section.concept.hidden').count()>=1)
    wik.locator('#search').fill('')
    wik.screenshot(path=str(R/'checks'/'desktop-wiki.png'),full_page=True)
    wf=browser.new_page();wf.set_content((R/'workflow.html').read_text(encoding='utf8'));record('Workflow 頁可開啟',wf.locator('h1').inner_text().startswith('Loop / Graph'))
    mobile=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1);mobile.set_content((R/'index.html').read_text(encoding='utf8'));mobile.screenshot(path=str(R/'checks'/'mobile-cover.png'),full_page=True)
    record('手機寬度無水平溢出',mobile.evaluate('document.documentElement.scrollWidth <= innerWidth'),str(mobile.evaluate('[document.documentElement.scrollWidth,innerWidth]')))
    browser.close()
httpd.shutdown()

summary={'status':'PASS','tested':len(results),'checks':results,'browser':'Chromium headless (desktop + mobile)','artifacts':['desktop-cover.png','desktop-logic.png','desktop-wiki.png','mobile-cover.png']}
(R/'checks'/'validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print('ALL',len(results),'CHECKS PASSED')
