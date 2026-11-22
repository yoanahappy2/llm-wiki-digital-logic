#!/usr/bin/env python3
"""Offline lint for source-card provenance, Wiki pages, and slide link graph.
The original remote source titles were verified manually; this script only checks local evidence.
"""
import pathlib,json,re,hashlib
R=pathlib.Path(__file__).resolve().parent
src=[json.loads(p.read_text(encoding='utf8')) for p in sorted((R/'raw').glob('S*.json'))]
audit=json.loads((R/'checks/source_audit.json').read_text(encoding='utf8'))
plan=json.loads((R/'slide_plan.json').read_text(encoding='utf8'))
checks=[]
def chk(title,truth,detail=''):
    checks.append({'check':title,'pass':bool(truth),'detail':str(detail)})
    if not truth:raise AssertionError(f'{title}: {detail}')
chk('5 份不同的來源網址',len(src)==len({s['url'] for s in src})==5)
chk('5 份非空 raw Markdown 來源卡',all((R/'raw'/f"{s['id']}.md").stat().st_size>350 for s in src))
chk('來源卡保持不可覆蓋性（SHA-256）',all(hashlib.sha256((R/item['raw_note']).read_bytes()).hexdigest()==item['sha256'] for item in audit['sources']))
chk('已改正 S05 網址與頁名',src[-1]['url'].endswith('/c6/c6s1/') and src[-1]['title'].startswith('6.1 Annotated Slides'))
known={s['concept_id'] for s in src}
index=(R/'wiki/index.md').read_text(encoding='utf8')
chk('index.md 索引 5 頁',all(f'[[{c}]]' in index for c in known))
for s in src:
    c=s['concept_id'];body=(R/'wiki'/f'{c}.md').read_text(encoding='utf8')
    chk(f'{c} Wiki 引用正確來源', f"[{s['id']}]" in body and s['url'] in body and body.startswith('# '+s['topic']))
    links=re.findall(r'\[\[(C\d{2})\]\]',body)
    chk(f'{c} Wiki 連結有效',len(links)>=1 and all(t in known for t in links))
    chk(f'{c} Wiki 完整教學結構', all(f'## {t}' in body for t in ['重要概念','檢查點','來源','相關頁面']))
chk('五份資料均被簡報引用',set(s['id'] for s in src)==set(x for sl in plan for x in sl.get('source_ids',[])))
trace=json.loads((R/'checks/slide_trace.json').read_text(encoding='utf8'))
chk('每頁簡報都有來源追溯紀錄',len(trace)==len(plan) and all(tr['slide_id']==sl['id'] for sl,tr in zip(plan,trace)))
chk('log.md 包含5次逐篇 ingest',sum(1 for l in (R/'wiki/log.md').read_text(encoding='utf8').splitlines() if l.startswith('## [2026-11-22] ingest |'))==5)
chk('預備流程包含來源失配證據', (R/'checks/source_mismatch_before.json').exists())
chk('網站不含未渲染的舊模板字串','{esc(' not in (R/'wiki.html').read_text(encoding='utf8'))
report={'status':'PASS','total':len(checks),'checks':checks,'limitation':'Source-title agreement at remote sites was manually verified, not automatically scraped in this offline script.'}
(R/'checks/lint_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('ALL',len(checks),'WIKI LINT CHECKS PASSED')
