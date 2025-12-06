from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from backend.services import parser, llm, notion

app = FastAPI()

# 1. API Endpoints
@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename
    content = await file.read()
    
    # 1. Extract Text
    extracted_text = ""
    if filename.lower().endswith(".pdf"):
        extracted_text = parser.extract_text_from_pdf(content)
    elif filename.lower().endswith((".ppt", ".pptx")):
        extracted_text = parser.extract_text_from_ppt(content)
    else:
        return JSONResponse(
            status_code=400,
            content={"error": True, "message": "不支援的檔案格式"}
        )

    # 2. Summarize
    summary = llm.summarize_content(extracted_text)

    # 3. Save to Notion (if summary is valid)
    notion_status = "Skipped (Summary failed)"
    if "Error" not in summary:
        notion_status = notion.create_notion_page(f"Note: {filename}", summary)

    return {
        "filename": filename,
        "summary": summary,
        "notion_status": notion_status
    }

# 2. Mount Static Files (Frontend) - Must be after API routes to avoid conflict
# This serves index.html at root "/"
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
