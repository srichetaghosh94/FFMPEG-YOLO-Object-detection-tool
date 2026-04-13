

# FFmpeg + YOLO Object Detection Tool

A desktop application built with Tkinter and FastAPI for:

* Extracting frames from videos using FFmpeg
* Running object detection on images using YOLO models
* Saving detection results (JSON + annotated images)

---

## Setup


### 1. Install dependencies

```
pip install -r requirements.txt
```

### 4. Install FFmpeg

install FFmpeg and add it to path:

```
ffmpeg -version
```

---

## Run

Start backend:

```
python -m uvicorn api:app --reload
```

Run GUI:

```
python main.py
```

---

## Notes

* YOLO models are downloaded automatically on first run
* Output files and model weights are not included in the repository
* Inference runs on CPU by default

---

## Project Structure

```
api.py
main.py
video_to_frames.py
object_detection.py
requirements.txt
README.md
```
