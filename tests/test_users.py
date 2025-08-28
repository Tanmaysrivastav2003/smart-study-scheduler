from fastapi.testclient import TestClient
from backend.app.main import app # Import your FastAPI app

# The TestClient allows us to make requests to our app without running a live server
client = TestClient(app)

def test_create_user_success():
    """
    Test that a user can be created successfully.
    """
    # Define the user data
    user_data = {
        "email": "test.success@example.com",
        "name": "Test Success User"
    }
    
    # Make the POST request
    response = client.post("/api/v1/users", json=user_data)
    
    # Assert that the request was successful
    assert response.status_code == 200
    
    # Assert that the returned data is correct
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert "id" in data
    assert "created_at" in data