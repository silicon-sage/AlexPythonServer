import requests
import pytest
import threading
import time
from app import create_app

class TestServer:
    def __init__(self, port=5001):
        self.port = port
        self.app = create_app()
        self.url = f"http://localhost:{port}"
        self.thread = None
        self.test_patient_id = "9000"
        
    def start(self):
        def run_app():
            self.app.run(port=self.port, use_reloader=False)
            
        self.thread = threading.Thread(target=run_app)
        self.thread.daemon = True
        self.thread.start()
        # Give the server a moment to start
        time.sleep(1)

    def stop(self):
        pass

@pytest.fixture(scope="session")
def api_server():
    server = TestServer()
    server.app.config['TESTING'] = True
    server.start()
    yield server
    server.stop()

@pytest.fixture(autouse=True)
def clear_data(api_server):
    response = requests.delete(f"{api_server.url}/health-records/{api_server.test_patient_id}")
    assert response.status_code == 200
    yield

def test_add_and_retrieve_lab_result(api_server):
    lab_data = {
        "type": "lab_result",
        "patient_id": api_server.patient_id,
        "value": "10.5",
        "description": "Blood Test",
        "provider": "Dr. Smith"
    }
    
    response = requests.post(
        f"{api_server.url}/health-records",
        json=lab_data
    )
    assert response.status_code == 201
    result = response.json()
    assert result["type"] == "lab_result"
    assert result["patient_id"] == api_server.test_patient_id
    
    response = requests.get(
        f"{api_server.url}/health-records",
        params={"patient_id": api_server.test_patient_id}
    )
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 1
    assert records[0]["type"] == "lab_result"
    assert records[0]["value"] == "10.5"

def test_add_prescription(api_server):
    prescription_data = {
        "type": "prescription",
        "patient_id": api_server.test_patient_id,
        "dose": "10mg",
        "drug": "Aspirin",
        "provider": "Dr. Jones"
    }
    
    response = requests.post(
        f"{api_server.url}/health-records",
        json=prescription_data
    )
    assert response.status_code == 201
    result = response.json()
    assert result["type"] == "prescription"
    assert result["drug"] == "Aspirin"

def test_invalid_record_type(api_server):
    invalid_data = {
        "type": "invalid_type",
        "patient_id": api_server.test_patient_id
    }
    
    response = requests.post(
        f"{api_server.url}/health-records",
        json=invalid_data
    )
    assert response.status_code == 400

def test_missing_required_fields(api_server):
    incomplete_data = {
        "type": "lab_result",
        # missing patient_id
        "value": 10.5
    }
    
    response = requests.post(
        f"{api_server.url}/health-records",
        json=incomplete_data
    )
    assert response.status_code == 400
