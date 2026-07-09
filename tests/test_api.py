from src.api.app import app

def test_api_predict_endpoint():
    client = app.test_client()
    with open("tests/fixtures/test.jpg", "rb") as img:
        response = client.post("/predict", data={"image": img})

    assert response.status_code == 200
    assert "masque_detecte" in response.get_json()

def test_api_predict_sans_image():
    client = app.test_client()
    response = client.post("/predict", data={})
    assert response.status_code == 400