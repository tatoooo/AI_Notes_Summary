from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# 🔥 FastAPI 的主應用程式，一定要在最外層
app = FastAPI()

# 找到 templates 資料夾，用來渲染 HTML
templates = Jinja2Templates(directory="templates")

# 首頁 GET /
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 接收上傳檔案的 API
@app.post("/upload-meeting", response_class=HTMLResponse)
async def upload_meeting(request: Request, file: UploadFile = File(...)):
    # 讀取上傳的檔案內容
    content = await file.read()
    size = len(content)

    # 回傳結果給前端 HTML 顯示
    result = {
        "message": "檔案收到！",
        "filename": file.filename,
        "size_bytes": size
    }

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result
        }
    )
