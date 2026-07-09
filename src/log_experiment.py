import mlflow
from src.predict import predict

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("pneumoscan-predictions")

with mlflow.start_run():
    resultats = predict("tests/fixtures/test.jpg")
    mlflow.log_param("modele", "yolov8m-seg.pt")
    mlflow.log_metric("nb_objets_detectes", len(resultats[0].boxes))
    mlflow.log_metric("masque_detecte", 1 if resultats[0].masks is not None else 0)
    print("Experience loggee dans MLflow")