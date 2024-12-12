import json
import pytest
from app.services.redis_service import get_redis_client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_lab_result(client, redis_mock):
    data = {
        "type": "lab_result",
        "patient_id": "123",
        "value": 10.5,
        "description": "Blood Test",
        "provider": "Dr. Smith"
    }
    
    response = client.post(
        '/health-records',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data['type'] == "lab_result"
    assert response_data['patient_id'] == "123"
    assert response_data['value'] == 10.5

def test_add_invalid_record_type(client, redis_mock):
    data = {
        "type": "invalid_type",
        "patient_id": "123"
    }
    
    response = client.post(
        '/health-records',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert b"Invalid record type" in response.data

def test_get_health_records_by_patient(client, redis_mock):
    # First add a record
    data = {
        "type": "lab_result",
        "patient_id": "123",
        "value": 10.5,
        "description": "Blood Test",
        "provider": "Dr. Smith"
    }
    
    client.post(
        '/health-records',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Then retrieve it
    response = client.get('/health-records?patient_id=123')
    assert response.status_code == 200
    records = json.loads(response.data)
    assert len(records) == 1
    assert records[0]['patient_id'] == "123"

def test_get_health_records_by_type(client, redis_mock):
    # Add a record
    data = {
        "type": "lab_result",
        "patient_id": "123",
        "value": 10.5,
        "description": "Blood Test",
        "provider": "Dr. Smith"
    }
    
    client.post(
        '/health-records',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Retrieve by type
    response = client.get('/health-records?type=lab_result')
    assert response.status_code == 200
    records = json.loads(response.data)
    assert len(records) == 1
    assert records[0]['type'] == "lab_result"