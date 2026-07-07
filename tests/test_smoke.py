from src.predict import predict

def test_pipeline_smoke():
    # Verifie que le pipeline tourne de bout en bout sans erreur.
    # L''image de test est generique (pas de radiographie pour l''instant),
    # donc on ne verifie pas encore la qualite de detection.
    resultats = predict("data/mini_sample/test.jpg")
    assert resultats is not None
    assert len(resultats) == 1
    assert resultats[0].boxes is not None