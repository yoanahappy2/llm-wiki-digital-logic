# 第十週作業｜LLM Wiki × HTML 教學簡報

**繳交標題：**中山大學［學號］人科大四［姓名］數位邏輯入門

### 1. Wiki 主題與介紹

我的主題是「從邏輯閘到有限狀態機：數位邏輯入門」。希望讓原本不了解數位電路的人，依序認識 AND、OR、NOT、XOR、半加器、D Flip-Flop、組合與時序邏輯，以及 FSM。我先決定初學者教學順序，再用 ChatGPT 逐篇整理來源、更新 Markdown Wiki，最後從 Wiki 概念頁製作互動式 HTML 教學簡報。

### 2. LLM Wiki 成果

共整理 **5 份不同教學來源**：S01–S03 為 Nand2Tetris 的 Boolean Logic、Boolean Arithmetic、Memory；S04–S05 為 MIT 6.004 的 Sequential Logic、Finite State Machines。每篇有 `raw/S0X.md` 來源卡、獨立的 `wiki/C0X.md` 概念頁，並保留網址、對應來源 ID、交叉連結。另有 `wiki/index.md` 作目錄、`wiki/log.md` 逐步記錄 ingest、query、lint。

**Wiki 網址：**［請貼上 GitHub Pages 的 wiki.html 實際網址］

### 3. HTML 教學簡報

依 Wiki 的五個主題整理成 **12 頁 HTML 簡報**，可用滑鼠或左右鍵翻頁；包括邏輯閘輸入切換、半加器運算、ON/OFF FSM 狀態切換、3 題小測驗。內容頁的 `[S01]`–`[S05]` 可以返回 Wiki 查到來源。

**簡報網址：**［請貼上 GitHub Pages 首頁實際網址］

### 4. Loop / Graph 工作流程

**先討論主題與教學對象 → 蒐集來源 → [來源標題/內容一致性檢查] → 逐篇 ingest 成 Wiki Markdown（更新 index/log）→ 查詢 Wiki → [核對引用、交叉連結及內容] → 產生 HTML 簡報 → [互動與手機測試]。**

如果來源與主題不符，回到「來源蒐集／核對」改正再 ingest；如果 Wiki 引用或計算不對，回到概念頁修正並重新 query；如果 HTML 內容或互動出錯，回到渲染節點重跑。這樣可把上游錯誤提前擋住，避免錯誤擴散到簡報。

**Graph／檢查頁：**［請貼上 GitHub Pages 的 workflow.html 實際網址］

### 5. 一次實際執行與檢查

本次先建立五份來源卡與五個概念頁，再以本地 Wiki 查詢三個問題：

1. 「XOR 跟 OR 有什麼不同？」→ 找到 `C01`，確認 A=B=1 時 OR=1、XOR=0。
2. 「半加器的進位如何算？」→ 找到 `C02`，確認 Carry=A AND B、Sum=A XOR B。
3. 「FSM 為什麼需要記住狀態？」→ 找到 `C05` 與 `C04`，確認狀態保存必要的輸入歷史。

查詢文字和引文保留在 `checks/query_results.json`。Wiki 靜態檢查共 **25 項通過**，包含來源數量、Markdown 資料卡、來源鏈、頁面引用與交叉連結；瀏覽器驗收另有 **22 項通過**，包括邏輯真值、半加器、FSM、翻頁、測驗與手機排版。結果在 `checks/lint_results.json` 與 `checks/validation.json`。

### 6. 反思與 Workflow 修正

本次最值得注意的是**來源核對節點**：原本第五份來源 S05 的主題寫成 FSM，但實際網址卻指向 MIT 第 9 章指令集設計，而正確的是第 6 章。我重新核對官方頁面、修正連結，因此把「來源標題、章節與主題是否相符」的檢查往前移到 ingest 之前。之前還遇過 Wiki HTML 顯示未展開的模板文字，因此在簡報生成之前加上模板檢查。這次把 workflow 改為 **先檢查來源 → 寫入 Wiki → 檢查 Wiki → 做簡報 → 測試**，而不是最後才一次檢查。

補充：LLM Wiki 採本地 Markdown 實作，來源卡是根據五份公開教材整理的中文摘要，而非複製五篇全文；LLM 撰寫與修改發生在本次 ChatGPT 協作中，離線查詢與測試工具則用於重現檢查。
