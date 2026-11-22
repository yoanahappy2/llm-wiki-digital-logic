# Week 10 — 數位邏輯 LLM Wiki × HTML 教學簡報（可交作業版）

整理五份公開教育資料的**中文來源卡**，再逐篇建立與修正持久化的 Markdown Wiki，最後由這個 Wiki 渲染教學 HTML。

## 檔案內容說明

- `index.html` — 可瀏覽的 **12 頁 HTML 教學簡報**（有邏輯閘、半加器、FSM 操作與小測驗）。
- `wiki.html` — 可搜尋的 **五個概念頁**，附來源鏈接。
- `workflow.html` — **loop / graph 及真實修正案例**。
- `submission.md` — **線上繳交文字**；部署 GitHub Pages 後填入三個實際 URL。

## 目錄與證據

```text
raw/S01.md ... S05.md         五份有來源網址的中文來源卡（非原文全文）
raw/S01.json ... S05.json     五份整理後的結構化來源資訊
wiki/C01.md ... C05.md       本次 LLM 撰寫的五個概念頁
wiki/index.md                持久化索引
wiki/log.md                  逐篇 ingest、三次 query、lint、修正紀錄
query_wiki.py                可重跑的簡單離線 Wiki 查詢（不是 LLM API）
lint_wiki.py                 來源/連結/引用/結構檢查
build.py                     讀取 Wiki Markdown 渲染 HTML，**不改寫 Wiki 內容**
validate.py                  Chromium 互動測試
checks/source_mismatch_before.json  修正前錯誤來源紀錄
checks/source_audit.json     五份來源逐筆核對／摘要卡 SHA-256
checks/query_results.json   三題查詢與對應的來源
checks/lint_results.json    Wiki 靜態 lint 結果
checks/slide_trace.json     各張簡報 → Wiki 頁面 → 來源 ID
checks/validation.json      實際 HTML/手機/互動測試
checks/wiki-before-fix.png  原始模板錯誤（前次）
checks/desktop-wiki.png     修正後 Wiki 頁面
```

## 如何重跑？（不需 API key）

使用 Python 3，安裝 `beautifulsoup4 playwright` 和 Chromium 後，在專案根目錄執行：

```bash
python3 query_wiki.py "半加器的進位如何算？"
python3 lint_wiki.py
python3 build.py
python3 validate.py
```

## 資料來源

- [S01 Nand2Tetris Boolean Logic](https://www.nand2tetris.org/project01)
- [S02 Nand2Tetris Boolean Arithmetic](https://www.nand2tetris.org/project02)
- [S03 Nand2Tetris Memory](https://www.nand2tetris.org/project03)
- [S04 MIT 6.004 Sequential Logic](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2009/resources/mit6_004s09_lec05/)
- [S05 MIT 6.004 Finite State Machines **第 6 章**](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c6/c6s1/)

