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
├── frontend/                 # Vue 3 + Vite 前端
│   ├── src/                  # Vue 組件源碼
│   │   ├── components/       # UI 組件 (FileUploader, FileList, SummaryResult)
│   │   ├── App.vue           # 主應用組件
│   │   └── main.js           # 應用入口
│   └── vite.config.js        # Vite 配置 (開發代理設定)
└── .env                      # 環境變數
```

## 快速開始

### 1. 安裝後端依賴

確保已安裝 Python 3.9+。

```bash
pip install -r requirements.txt
# 或者手動安裝：
# pip install fastapi uvicorn python-dotenv google-generativeai notion-client pypdf python-pptx python-multipart
```

### 2. 安裝前端依賴

```bash
cd frontend
npm install
```

### 3. 設定環境變數

在根目錄建立 `.env` 檔案（參考範例）：

```ini
GEMINI_API_KEY=AIza...              # Google Gemini API Key
NOTION_API_KEY=secret_...           # Notion Integration Token
NOTION_DATABASE_ID=...              # 目標 Notion Database ID
```

> **注意**: 您的 Notion Integration 必須已被邀請至該 Database，否則無法寫入。

### 4. 啟動服務

**方式 A: 完整開發環境（推薦）**

同時啟動前後端開發伺服器：

```bash
# Terminal 1: 啟動後端 (port 8000)
uvicorn backend.main:app --reload

# Terminal 2: 啟動前端 (port 5173)
cd frontend
npm run dev
```

前端訪問：👉 [http://localhost:5173](http://localhost:5173)
（Vite 會自動將 `/api` 請求代理到後端 8000 port）

**方式 B: 生產模式預覽**

先建置前端，再由 FastAPI 統一服務：

```bash
# 建置前端
cd frontend
npm run build

# 啟動後端（會自動掛載前端靜態檔案）
cd ..
uvicorn backend.main:app
```

訪問：👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 開發者筆記

### 後端開發
- 若要更換 AI 模型，請修改 `backend/services/llm.py` 中的 `GenerativeModel` 參數。
- API 端點位於 `backend/main.py`，使用 FastAPI 自動生成的文檔：`/docs`

### 前端開發
- 使用 Vue 3 Composition API (`<script setup>`)
- 開發時修改 `frontend/src/` 下的檔案，Vite HMR 會即時更新
- Vite proxy 配置位於 `frontend/vite.config.js`，開發環境自動將 `/api` 轉發至後端

### 架構說明
- **開發環境**: 前端 Vite dev server (5173) + 後端 FastAPI (8000)，透過 Vite proxy 避免 CORS
- **生產環境**: 前端建置為靜態檔案，由 FastAPI `StaticFiles` 掛載，單一服務統一對外
