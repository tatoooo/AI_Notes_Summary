# AI Note Summary (AI 筆記摘要助手)

一個基於 Google Gemini 1.5 Flash 模型的智慧筆記摘要工具。
能夠自動解析 PDF 與 PowerPoint 投影片，生成結構化 Markdown 摘要，並自動同步到 Notion 資料庫。

## 核心功能

- **多格式支援**: 拖曳上傳 PDF (`.pdf`) 或 PowerPoint (`.ppt`, `.pptx`) 檔案。
- **AI 智慧摘要**: 使用 Google Gemini 1.5 Flash 快速生成精準的結構化重點摘要。
- **Notion 同步**: 自動將生成的摘要以 Page 形式寫入指定的 Notion Database。
- **現代化介面**: 乾淨、響應式的單頁應用 (SPA) 設計。

## 系統架構

本專案採用前後端分離的模組化架構：

```text
├── backend/                  # Python FastAPI 後端
│   ├── main.py               # API 入口
│   ├── config.py             # 設定檔管理
│   └── services/             # 核心服務層
│       ├── llm.py            # Gemini AI 整合
│       ├── parser.py         # 檔案解析邏輯 (PDF/PPT)
│       └── notion.py         # Notion API 整合
├── frontend/                 # 靜態前端 (HTML/CSS/JS)
└── .env                      # 環境變數
```

## 快速開始

### 1. 安裝依賴

確保已安裝 python 3.9+。

```bash
pip install -r requirements.txt
# 或者手動安裝：
# pip install fastapi uvicorn python-dotenv google-generativeai notion-client pypdf python-pptx python-multipart
```

### 2. 設定環境變數

在根目錄建立 `.env` 檔案（參考範例）：

```ini
GEMINI_API_KEY=AIza...              # Google Gemini API Key
NOTION_API_KEY=secret_...           # Notion Integration Token
NOTION_DATABASE_ID=...              # 目標 Notion Database ID
```

> **注意**: 您的 Notion Integration 必須已被邀請至該 Database，否則無法寫入。

### 3. 啟動服務

使用 Uvicorn 啟動後端伺服器：

```bash
uvicorn backend.main:app --reload
```

服務啟動後，請打開瀏覽器訪問：
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 開發者筆記

- 若要更換 AI 模型，請修改 `backend/services/llm.py` 中的 `GenerativeModel` 參數。
- 前端檔案位於 `frontend/`，修改後重新整理瀏覽器即可看到變更（靜態檔案由 FastAPI 掛載）。
