import pytest
from datetime import datetime
from app.models.health_records import (
    LabResult, Prescription, AppointmentNote, SelfMeasurement
)

def test_lab_result_creation():
    lab_result = LabResult(
        patient_id="123",
        value=10.5,
        description="Blood Test",
        provider="Dr. Smith"
    )
    
    data = lab_result.to_dict()
    assert data['type'] == "lab_result"
    assert data['patient_id'] == "123"
    assert data['value'] == 10.5
    assert data['description'] == "Blood Test"
    assert data['provider'] == "Dr. Smith"
    assert isinstance(datetime.fromisoformat(data['timestamp']), datetime)

def test_prescription_creation():
    prescription = Prescription(
        patient_id="123",
        dose="10mg",
        drug="Aspirin",
        provider="Dr. Smith"
    )
    
    data = prescription.to_dict()
    assert data['type'] == "prescription"
    assert data['patient_id'] == "123"
    assert data['dose'] == "10mg"
    assert data['drug'] == "Aspirin"
    assert data['provider'] == "Dr. Smith"

def test_appointment_note_creation():
    note = AppointmentNote(
        patient_id="123",
        note="Regular checkup",
        provider="Dr. Smith"
    )
    
    data = note.to_dict()
    assert data['type'] == "appointment_note"
    assert data['patient_id'] == "123"
    assert data['note'] == "Regular checkup"
    assert data['provider'] == "Dr. Smith"

def test_self_measurement_creation():
    measurement = SelfMeasurement(
        patient_id="123",
        value=98.6,
        description="Temperature",
        provider="Patient"
    )
    
    data = measurement.to_dict()
    assert data['type'] == "self_measurement"
    assert data['patient_id'] == "123"
    assert data['value'] == 98.6
    assert data['description'] == "Temperature"
    assert data['provider'] == "Patient"