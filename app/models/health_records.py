from datetime import datetime
import uuid
from typing import Dict

class HealthRecord:
    def __init__(self, record_type: str, patient_id: str, provider: str = None, timestamp: datetime = None):
        self.id = str(uuid.uuid4())
        self.record_type = record_type
        self.patient_id = patient_id
        self.provider = provider
        self.timestamp = timestamp or datetime.now()

class LabResult(HealthRecord):
    def __init__(self, patient_id: str, value: float, description: str, provider: str = None):
        super().__init__("lab_result", patient_id, provider)
        self.value = value
        self.description = description

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.record_type,
            "patient_id": self.patient_id,
            "provider": self.provider,
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "description": self.description
        }

class Prescription(HealthRecord):
    def __init__(self, patient_id: str, dose: str, drug: str, provider: str = None):
        super().__init__("prescription", patient_id, provider)
        self.dose = dose
        self.drug = drug

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.record_type,
            "patient_id": self.patient_id,
            "provider": self.provider,
            "timestamp": self.timestamp.isoformat(),
            "dose": self.dose,
            "drug": self.drug
        }

class AppointmentNote(HealthRecord):
    def __init__(self, patient_id: str, note: str, provider: str = None):
        super().__init__("appointment_note", patient_id, provider)
        self.note = note

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.record_type,
            "patient_id": self.patient_id,
            "provider": self.provider,
            "timestamp": self.timestamp.isoformat(),
            "note": self.note
        }

class SelfMeasurement(HealthRecord):
    def __init__(self, patient_id: str, value: float, description: str, provider: str = None):
        super().__init__("self_measurement", patient_id, provider)
        self.value = value
        self.description = description

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.record_type,
            "patient_id": self.patient_id,
            "provider": self.provider,
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "description": self.description
        }