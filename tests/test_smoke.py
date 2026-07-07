from src.predict import predict

def test_pipeline_smoke():
    resultats = predict("tests/fixtures/test.jpg")
    assert resultats is not None
    assert len(resultats) == 1
    assert resultats[0].boxes is not None
    # Volontairement force a echouer, pour verifier
    # que le pipeline detecte bien un probleme.
    assert resultats[0].masks is not None, "aucun masque detecte"