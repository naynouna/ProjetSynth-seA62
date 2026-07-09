from flask import Flask, request, jsonify
from src.predict import predict
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "<h1>PneumoScan IA</h1><p>Envoyez une image en POST sur /predict</p>"

@app.route("/predict", methods=["POST"])
def predict_route():
    if "image" not in request.files:
        return jsonify({"erreur": "aucune image envoyee"}), 400

    fichier = request.files["image"]
    chemin_temp = "temp_upload.jpg"
    fichier.save(chemin_temp)

    resultats = predict(chemin_temp)
    masque_detecte = resultats[0].masks is not None

    os.remove(chemin_temp)

    return jsonify({
        "masque_detecte": masque_detecte,
        "nb_objets_detectes": len(resultats[0].boxes)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)