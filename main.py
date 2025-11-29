from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model.model import corrupt_image as model_corrupt_image

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"
INDEX_FILE = TEMPLATES_DIR / "index.html"
DEFAULT_IMAGE = DATA_DIR / "Set12" / "01.png"
DEFAULT_IMAGE_RELATIVE = str(DEFAULT_IMAGE.relative_to(DATA_DIR))
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

app = FastAPI(title="Image Denoiser API")


@app.get("/api/ping", response_class=PlainTextResponse)
async def ping() -> PlainTextResponse:
    return PlainTextResponse("Server responded successfully")


@app.post("/api/upload", response_class=PlainTextResponse)
async def upload_image(file: UploadFile = File(...)) -> PlainTextResponse:
    # do image logic here
    msg = f"Image '{file.filename}' received successfully"
    return PlainTextResponse(msg)


def _list_images() -> list[str]:
    if not DATA_DIR.exists():
        return []

    return sorted(
        str(path.relative_to(DATA_DIR))
        for path in DATA_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def _image_options() -> list[dict[str, str]]:
    return [
        {
            "label": "Corrupt",
            "endpoint": "/actions/corrupt",
            "method": "post",
            "type": "process",
        },
        {
            "label": "Reset",
            "type": "reset",
        },
    ]


@app.get("/get-image-dropdown", response_class=HTMLResponse)
async def get_images(request: Request) -> HTMLResponse:
    images = _list_images()
    return templates.TemplateResponse(
        "components/dropdown.jinja",
        {"request": request, "images": images},
    )


@app.get("/select-image", response_class=FileResponse)
async def select_image(img: str = "") -> FileResponse:
    if not img:
        return FileResponse(DEFAULT_IMAGE)

    image_path = (DATA_DIR / img).resolve()

    try:
        image_path.relative_to(DATA_DIR)
    except ValueError:
        return FileResponse(DEFAULT_IMAGE)

    if not image_path.exists():
        return FileResponse(DEFAULT_IMAGE)

    return FileResponse(image_path)


@app.post("/actions/corrupt")
async def corrupt_image(file: UploadFile = File(...)) -> Response:
    image_bytes = await file.read()
    processed = model_corrupt_image(image_bytes)
    media_type = file.content_type or "image/png"
    return Response(content=processed, media_type=media_type)


@app.get("/", include_in_schema=False)
async def serve_index(request: Request):
    if not INDEX_FILE.exists():
        return JSONResponse({"detail": "index.html not found"}, status_code=404)

    images = _list_images()
    image_options = _image_options()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "images": images,
            "image_options": image_options,
            "default_image": DEFAULT_IMAGE_RELATIVE,
        },
    )


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def main():
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)


if __name__ == "__main__":
    main()
