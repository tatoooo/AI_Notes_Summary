# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Note Summary (AI 筆記摘要助手) - An intelligent note summarization tool that:
- Accepts PDF and PowerPoint uploads
- Uses Google Gemini 1.5 Flash to generate structured Markdown summaries
- Automatically syncs summaries to a Notion database

## Architecture

**Three-layer service architecture:**

1. **API Layer** (`backend/main.py`): FastAPI application with single `/api/upload` endpoint
2. **Service Layer** (`backend/services/`):
   - `parser.py`: Document parsing (PDF via pypdf, PPT via python-pptx)
   - `llm.py`: Gemini API integration for summarization
   - `notion.py`: Notion API integration for page creation
3. **Frontend**: Static HTML/CSS/JS served via FastAPI's StaticFiles mount

**Request Flow:**
`upload` → `extract text` → `summarize (Gemini)` → `create Notion page` → `return JSON response`

## Environment Configuration

Required environment variables in `.env`:
```ini
GEMINI_API_KEY=AIza...              # Google Gemini API Key
NOTION_API_KEY=secret_...           # Notion Integration Token
NOTION_DATABASE_ID=...              # Target Notion Database ID
```

Configuration is managed through `backend/config.py` using `python-dotenv`.

## Development Commands

### Start Development Server
```bash
uvicorn backend.main:app --reload
```
Access at: http://127.0.0.1:8000

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Docker Build & Run
```bash
docker build -t ai-notes-summary .
docker run -p 8000:8000 --env-file .env ai-notes-summary
```

## Key Implementation Details

### LLM Service (`services/llm.py`)
- Model: `gemini-1.5-flash`
- Content truncated to 15,000 characters to avoid context limits
- Structured prompt requests H2 headings, bullet points, and bold keywords for Notion compatibility

### Notion Service (`services/notion.py`)
- Creates pages with `Name` property (title field)
- Content stored as paragraph block (limited to 2,000 characters)
- **Important**: Notion Integration must be invited to target database before write access works

### File Parsing (`services/parser.py`)
- PDF: Uses `pypdf.PdfReader` to extract text page-by-page
- PPT/PPTX: Uses `python-pptx.Presentation` to extract shape text from each slide
- Both return concatenated text strings

### Static Files Mounting
Frontend is mounted **after** API routes in `main.py` to prevent route conflicts. The `html=True` parameter enables serving `index.html` at root path.

## Language

Project documentation and user-facing content is in Traditional Chinese (繁體中文).
