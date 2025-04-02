import mongoengine
from mongoengine import Document, StringField
from fastapi import FastAPI, File, UploadFile
import base64

# Connect to MongoDB
mongoengine.connect("classroom", host="mongodb://localhost:27017/Video")

app = FastAPI()

def image_to_base64(file):
    return base64.b64encode(file.read()).decode("utf-8")


class Video(Document):
    title = StringField(required=True, unique=True)
    file_base64 = StringField(required=True)

    meta = {"collection": "Videos"}


@app.post("/upload_video")
async def upload_video(title: str, file: UploadFile = File(...)):
    file_base64 = image_to_base64(file.file)

    existing_video = Video.objects(title=title).first()
    if existing_video:
        return {"error": "A video with this title already exists!"}

    # Save to MongoDB
    video = Video(title=title, file_base64=file_base64)
    video.save()

    return {"message": "Video uploaded successfully", "title": title}


@app.get("/get_video")
def get_video():
    videos = Video.objects()

    if not videos:
        return {"error": "No videos found"}

    result = [{"title": video.title, "file_base64": video.file_base64} for video in videos]

    return {"videos": result}
