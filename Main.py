import mongoengine
from mongoengine import Document, StringField
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import base64

mongoengine.connect("classroom", host="mongodb+srv://naveen:Naveen1122@cluster0.pghl7v8.mongodb.net/")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Images(Document):
    title = StringField(required=True, unique=True)
    image_data = StringField(required=True)
    meta = {"collection": "Images"}


@app.post("/upload_images")
async def upload_images(title: str, file: UploadFile = File(...)):
    content = await file.read()
    base64_encoded = base64.b64encode(content).decode("utf-8")

    Images(title=title, image_data=base64_encoded).save()

    return JSONResponse(content={"message": "Image uploaded successfully", "title": title})


@app.get("/get_images")
async def get_images():
    images = Images.objects()
    image_list = [{"title": img.title, "base64": img.image_data} for img in images]
    return JSONResponse(content={"images": image_list})
