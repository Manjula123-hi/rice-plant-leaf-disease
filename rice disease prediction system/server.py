import uvicorn
from fastapi import FastAPI, UploadFile, File
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import cv2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("./best_model.h5")
CLASS_NAMES = [("bacterial leaf blight", 0),
               ("brown spot", 1),
               ("healthy", 2),
               ("leaf blast", 3),
               ("leaf scald", 4),
               ("narrow brown spot", 5)]

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

def preprocess_image(image) -> np.ndarray:
    image = cv2.resize(image, (256, 256), interpolation = cv2.INTER_AREA)
    return image.astype(np.float32) / 255.

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    image = preprocess_image(image)
    img_batch = np.expand_dims(image, 0)
    prediction = MODEL.predict(img_batch)
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    predicted_class_name = CLASS_NAMES[predicted_class_index][0]
    confidence = float(prediction[0][predicted_class_index])
    return {
            "class_name": predicted_class_name, 
            "confidence": confidence
            }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
