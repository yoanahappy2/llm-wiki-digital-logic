#!/usr/bin/env python3
"""Offline Wiki search demonstration: reads index.md then the linked Markdown pages.
No model inference/API at runtime. Human/LLM-authored answers are recorded separately.
"""
import pathlib,re,json,sys
R=pathlib.Path(__file__).resolve().parent
INDEX=(R/'wiki/index.md').read_text(encoding='utf8')
PAGES={cid:(R/'wiki'/f'{cid}.md').read_text(encoding='utf8') for cid in re.findall(r'\[\[(C\d{2})\]\]',INDEX)}
KEYS={'XOR':['xor','or','相同','不同'],'半加器':['半加器','sum','carry','進位','全加器'],'FSM':['fsm','狀態','轉移','記憶'],'DFF':['dff','正緣','時鐘','儲存']}
def query(q):
    words=[]
    for k,v in KEYS.items():
        if k.casefold() in q.casefold() or any(w in q.casefold() for w in v[:2]):words.extend(v)
    if not words: words=re.findall(r'[A-Za-z]+|[\u4e00-\u9fff]{2,}',q)
    scored=[]
    for cid,body in PAGES.items():
        score=sum((3 if term.casefold() in body.split('## 重要概念')[0].casefold() else 1) for term in words if term.casefold() in body.casefold())
        if score:
            src=re.search(r'\[(S\d{2})\]',body)
            scored.append({'page':f'wiki/{cid}.md','title':body.splitlines()[0][2:],'source_id':src.group(1) if src else None,'match_score':score,'excerpt':body.split('## 重要概念\n',1)[1].split('\n## ',1)[0].strip()[:280]})
    return sorted(scored,key=lambda x:(-x['match_score'],x['page']))[:3]
if __name__=='__main__':
    for q in sys.argv[1:] or ['XOR 跟 OR 有什麼不同？','半加器的進位如何算？','FSM 為什麼需要記住狀態？']:
        print(json.dumps({'query':q,'retrieved':query(q)},ensure_ascii=False,indent=2))
