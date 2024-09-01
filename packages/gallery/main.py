import logging
import os

import aiofiles
from fastapi import FastAPI, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.security import APIKeyHeader
from pathvalidate import sanitize_filename
from pydantic import BaseModel
from starlette import status

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)

app = FastAPI()

GALLERY_KEY = os.getenv("GALLERY_KEY")
api_key_scheme = APIKeyHeader(name="gallery_key")

STORAGE_DIRECTORY = os.getenv("STORAGE_DIRECTORY")
os.makedirs(STORAGE_DIRECTORY, exist_ok=True)


@app.post("/upload")
async def upload(file: UploadFile, gallery_key: str = Depends(api_key_scheme)):
    logger.info(f"( ) upload request received for {file.filename}")
    if gallery_key != GALLERY_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid gallery key")
    if file.content_type != "image/png":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="upload only accepts png files")
    if file.filename != sanitize_filename(file.filename):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid filename")
    storage_path = f"{STORAGE_DIRECTORY}/{file.filename}"
    async with aiofiles.open(f"{STORAGE_DIRECTORY}/{file.filename}", mode="wb") as output_file:
        while content := await file.read(1024):
            await output_file.write(content)
    logger.info(f"(*) uploaded file to: {storage_path}")
    return {"success": True}


class DownloadRequest(BaseModel):
    file_name: str


@app.post("/download")
async def download(request: DownloadRequest, gallery_key: str = Depends(api_key_scheme)):
    logger.info(f"( ) download request received for {request.file_name}")
    if gallery_key != GALLERY_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid gallery key")
    if request.file_name != sanitize_filename(request.file_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid filename")
    storage_path = f"{STORAGE_DIRECTORY}/{request.file_name}"
    if not os.path.exists(storage_path):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="file does not exist")
    logger.info(f"(*) returning file {storage_path}")
    return FileResponse(storage_path)
