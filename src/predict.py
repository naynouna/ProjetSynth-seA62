from ultralytics import YOLO

MODEL_PATH = "yolov8m-seg.pt"

def predict(image_path):
    model = YOLO(MODEL_PATH)
    resultats = model.predict(image_path, verbose=False)
    return resultats