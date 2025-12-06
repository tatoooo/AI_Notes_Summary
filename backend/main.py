from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from backend.services import parser, llm, notion

app = FastAPI()

from typing import List

# 1. API Endpoints
@app.post("/api/upload")
async def upload_document(files: List[UploadFile] = File(...)):
    combined_text = ""
    file_names = []

    for file in files:
        filename = file.filename
        file_names.append(filename)
        content_bytes = await file.read()
            
        extracted_text = ""
        try:
            if filename.lower().endswith(".pdf"):
                extracted_text = parser.extract_text_from_pdf(content_bytes)
            elif filename.lower().endswith((".ppt", ".pptx")):
                extracted_text = parser.extract_text_from_ppt(content_bytes)
            elif filename.lower().endswith((".mp3", ".wav", ".m4a", ".ogg")):
                # Audio uses Gemini via llm.py
                # Reset file position because we read it above (though we didn't use it for audio)
                # But UploadFile.read() moves the cursor.
                await file.seek(0)
                extracted_text = llm.transcribe_audio(file)
            else:
                print(f"Skipping unsupported file: {filename}")
                continue
            
            if extracted_text:
                combined_text += f"\n\n--- Source: {filename} ---\n\n" + extracted_text
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    if not combined_text:
        return JSONResponse(
            status_code=400,
            content={"error": True, "message": "無法提取有效內容或格式不支援"}
        )

    # 2. Summarize
    summary = llm.summarize_content(combined_text)

    # 3. Save to Notion (if summary is valid)
    notion_status = "Skipped (Summary failed)"
    title = f"Note: {', '.join(file_names)}"
    if len(title) > 100:
        title = title[:97] + "..."
        
    if "Error" not in summary:
        notion_status = notion.create_notion_page(title, summary)

    return {
        "filename": ", ".join(file_names),
        "summary": summary,
        "notion_status": notion_status
    }

# 2. Mount Static Files (Frontend) - Must be after API routes to avoid conflict
# This serves index.html at root "/"
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
