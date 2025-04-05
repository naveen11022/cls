

from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os

app = FastAPI()

directory = "static/images"
os.makedirs(directory, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/uploads")
def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(directory, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return JSONResponse(content={
        "message": "File uploaded successfully",
        "filename": file.filename,
        "image_url": f"/static/images/{file.filename}"
    })


@app.get("/send_images")
def send_images():
    image_folder = []

    for image_name in os.listdir(directory):
        image_folder.append({
            "title": os.path.splitext(image_name)[0],
            "image_url": f"/static/images/{image_name}"
        })

    return JSONResponse(content={"images": image_folder})
