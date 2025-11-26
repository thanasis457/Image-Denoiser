from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
INDEX_FILE = FRONTEND_DIR / "index.html"

app = FastAPI(title="Image Denoiser API")


@app.get("/api/ping", response_class=PlainTextResponse)
async def ping() -> PlainTextResponse:
    # htmx will insert this directly into the #status element
    return PlainTextResponse("Server responded successfully")


@app.post("/api/upload", response_class=PlainTextResponse)
async def upload_image(file: UploadFile = File(...)) -> PlainTextResponse:
    # Placeholder: in a real application we would process the uploaded image.
    msg = f"Image '{file.filename}' received successfully"
    return PlainTextResponse(msg)


@app.get("/", include_in_schema=False)
async def serve_index():
    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE)
    return JSONResponse({"detail": "index.html not found"}, status_code=404)


app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


def main():
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)


if __name__ == "__main__":
    main()
