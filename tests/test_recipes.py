from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_recipes_empty():
    response = client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []


def test_create_recipe():
    data = {
        "name": "Test Recipe",
        "time_minutes": 10,
        "description": "Simple test recipe",
        "ingredients": [{"name": "Sugar", "amount": "1 tbsp"}],
    }
    response = client.post("/recipes", json=data)
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == data["name"]
    assert result["ingredients"][0]["name"] == "Sugar"
