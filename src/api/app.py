from flask import Flask, request, jsonify, render_template_string
from src.predict import predict
import os

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>PneumoScan</title>
<style>
body { font-family: -apple-system, Segoe UI, Arial, sans-serif; background: #141E3C; color: #fff; margin: 0; display: flex; flex-direction: column; align-items: center; padding: 50px 20px; }
h1 { margin: 10px 0 5px; font-size: 28px; }
p.subtitle { color: #9AA6C4; margin-top: 0; }
.card { background: #1F2E56; border-radius: 16px; padding: 30px; max-width: 480px; width: 100%; margin-top: 30px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
#dropzone { border: 2px dashed #0E8C86; border-radius: 12px; padding: 40px 20px; text-align: center; cursor: pointer; transition: background 0.2s; }
#dropzone:hover { background: rgba(14,140,134,0.1); }
#dropzone.dragover { background: rgba(14,140,134,0.2); }
input[type=file] { display: none; }
button { background: #0E8C86; color: #fff; border: none; padding: 12px 24px; border-radius: 8px; font-size: 15px; cursor: pointer; margin-top: 16px; width: 100%; }
button:disabled { opacity: 0.5; cursor: not-allowed; }
#preview { max-width: 100%; border-radius: 8px; margin-top: 16px; display: none; }
#result { margin-top: 20px; padding: 16px; border-radius: 8px; background: #141E3C; display: none; font-size: 14px; line-height: 1.6; }
.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
.badge.oui { background: #B14328; }
.badge.non { background: #2E8B57; }
</style>
</head>
<body>
<h1>PneumoScan</h1>
<p class="subtitle">Analyse automatique de radiographies thoraciques</p>
<div class="card">
<div id="dropzone">
<p>Glissez une radiographie ici<br>ou cliquez pour en choisir une</p>
<input type="file" id="fileInput" accept="image/*">
</div>
<img id="preview">
<button id="submitBtn" disabled>Analyser l'image</button>
<div id="result"></div>
</div>
<script>
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const submitBtn = document.getElementById('submitBtn');
const resultBox = document.getElementById('result');
let selectedFile = null;
dropzone.addEventListener('click', () => fileInput.click());
dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
dropzone.addEventListener('drop', e => { e.preventDefault(); dropzone.classList.remove('dragover'); handleFile(e.dataTransfer.files[0]); });
fileInput.addEventListener('change', e => handleFile(e.target.files[0]));
function handleFile(file) {
  if (!file) return;
  selectedFile = file;
  preview.src = URL.createObjectURL(file);
  preview.style.display = 'block';
  submitBtn.disabled = false;
  resultBox.style.display = 'none';
}
submitBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  submitBtn.disabled = true;
  submitBtn.textContent = "Analyse en cours...";
  const formData = new FormData();
  formData.append('image', selectedFile);
  try {
    const res = await fetch('/predict', { method: 'POST', body: formData });
    const data = await res.json();
    const badge = data.masque_detecte
      ? '<span class="badge oui">Zone d\u00e9tect\u00e9e</span>'
      : '<span class="badge non">Aucune zone</span>';
    resultBox.innerHTML = '<strong>R\u00e9sultat</strong><br>Zone d\u00e9tect\u00e9e : ' + badge + '<br>Objets d\u00e9tect\u00e9s : ' + data.nb_objets_detectes;
    resultBox.style.display = 'block';
  } catch (err) {
    resultBox.innerHTML = "Erreur lors de l'analyse.";
    resultBox.style.display = 'block';
  }
  submitBtn.disabled = false;
  submitBtn.textContent = "Analyser l'image";
});
</script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(PAGE)

@app.route("/predict", methods=["POST"])
def predict_route():
    if "image" not in request.files:
        return jsonify({"erreur": "aucune image envoyee"}), 400
    fichier = request.files["image"]
    chemin_temp = "temp_upload.jpg"
    fichier.save(chemin_temp)
    resultats = predict(chemin_temp)
    masque_detecte = len(resultats[0].boxes) > 0
    os.remove(chemin_temp)
    return jsonify({"masque_detecte": masque_detecte, "nb_objets_detectes": len(resultats[0].boxes)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
