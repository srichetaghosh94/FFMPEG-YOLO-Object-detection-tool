from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from ultralytics import YOLO
import shutil
import os
import uuid
import cv2

app = FastAPI()

models = {
    "yolov8": YOLO("yolov8n.pt"),
    "yolov5": YOLO("yolov5s.pt")
}

UPLOAD_DIR = "temp_uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.post("/predict")
async def predict(
    files: List[UploadFile] = File(...),
    model: str = Form(...)
):
    model = models[model]

    results_output = {}
    annotated_files = []

    for file in files:
        file_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_DIR, file_id + "_" + file.filename)

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # run inference
        results = model(input_path)

        img = cv2.imread(input_path)

        detections = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf)
                cls = int(box.cls)
                label = model.names[cls]

                # draw bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    img,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

                detections.append({
                    "label": label,
                    "confidence": conf,
                    "bbox": [x1, y1, x2, y2]
                })

        #output_path = os.path.join(OUTPUT_DIR, file_id + "_out.jpg")
        original_name = os.path.splitext(file.filename)[0]
        output_filename = f"{original_name}_annotated.jpg"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        cv2.imwrite(output_path, img)

        results_output[file.filename] = {
            "detections": detections,
            "annotated_image": output_path
        }

        os.remove(input_path)

    return results_output