from ultralytics import YOLO

MODEL_PATH = "models/best.pt"

def predict(image_path):
    model = YOLO(MODEL_PATH)
    resultats = model.predict(image_path, verbose=False)
    return resultats