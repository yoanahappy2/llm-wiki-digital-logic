# LLM Wiki 專案協作規則（數位邏輯入門）

## 目標

從已核對的公開教學來源整理出持久化 Markdown Wiki；使用 Wiki 內容製作可瀏覽的 HTML 教學簡報。讓不懂數位邏輯的初學者可學到 AND / OR / XOR、半加器、DFF、時序電路、FSM。

## 權限與資料邊界

- `raw/` 是來源卡和來源 metadata。**不可改動已核對的原始摘要卡**；如來源確實有誤，先寫 `checks/` 的修正證據，再明確更新 metadata 與對應來源卡並重算 `source_audit.json` SHA-256。
- `wiki/C*.md`、`wiki/index.md` 由 LLM 協助撰寫、更新；每個重要結論都要有 `[Sxx]` 來源標記。
- 對外公開專案只存本次撰寫的中文原創摘要，不擅自複製整篇教材原文或他人簡報。
- 不可把未驗證的公式、教材原例題、測試通過與工具執行紀錄寫成既成事實。

## 先討論再生成

1. 先決定受眾：完全沒有數位電路背景的學習者；範圍五個概念主題。
2. 把五份不同教材 URL 核對**頁面標題／章節／實際主題**；若不相符，回到蒐集階段。
3. 逐篇讀取 `raw/Sxx.md`，再建立或更新 `wiki/Cxx.md`；更新 `wiki/index.md` 與追加 `wiki/log.md`。
4. Query：先讀 `wiki/index.md`，再查所需概念頁；回答要引用 Wiki 概念頁與 `[Sxx]`。
5. Lint：每次修改後驗證來源鏈、概念互相連結、公式和簡報頁對應。若失敗，回到對應節點重新修改。
6. 確認 Wiki 通過後執行 `python3 build.py` 產生 `wiki.html`、`index.html` 和 `workflow.html`；這個程式**不能覆寫 wiki Markdown**。
7. 最後執行 `python3 lint_wiki.py` 與 `python3 validate.py`，不能憑印象聲稱測試通過。

## 核心檢查

- S05 必須指向 MIT 6.004 **6.1 Finite State Machines**，不可誤連 9.1 指令集。
- OR 與 XOR 不可混淆；半加器 Sum=A XOR B，Carry=A AND B。
- DFF 教學範例為**正緣觸發**，不是對所有 DFF 的通稱；並且不要聲稱所有時序電路都一定使用時鐘。
- ON/OFF 燈光 FSM 是本專題自行設計的互動例子，不是 MIT 組合鎖原始例題。

## 驗收標準

5 份獨立來源卡、5 個有來源標記的 Wiki 概念頁、可搜尋的 Wiki HTML、12 頁可操作教學簡報、來源對應、Query/Lint 紀錄，公開前必須由使用者自己部署並實際點開 GitHub Pages 驗證。
