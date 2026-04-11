from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app

# Create a testing client for our FastAPI app
client = TestClient(app)

@patch("backend.pipeline.generate_explanation")
def test_forecast_endpoint_success(mock_generate):
    mock_generate.return_value = "This is a mocked explanation."
    
    response = client.post(
        "/forecast",
        json={
            "values": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify the JSON response structure is correct
    assert "forecast" in data
    assert "model_selected" in data
    assert "features" in data
    assert data["explanation"] == "This is a mocked explanation."


def test_csv_upload_missing_column():
    dummy_file = ("dummy.csv", b"col1,col2\n1,2", "text/csv")
    
    response = client.post(
        "/forecast/csv",
        files={"file": dummy_file}
    )
    assert response.status_code == 400
    assert "target_column" in response.json()["detail"]
