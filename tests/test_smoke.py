import glob
from src.predict import predict

def test_pipeline_smoke():
    # Utilise les donnees recuperees par DVC depuis Google Cloud,
    # pas une fixture Git separee - preuve que le mecanisme est reellement branche.
    images = sorted(glob.glob("data/dvc_sample/*.jpg"))
    assert len(images) > 0, "aucune image DVC trouvee - dvc pull a-t-il ete lance ?"

    resultats = predict(images[0])
    assert resultats is not None
    assert len(resultats) == 1
    assert resultats[0].boxes is not None