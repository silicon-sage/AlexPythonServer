from flask import Flask, request, jsonify, render_template, render_template_string
from datetime import datetime
from typing import List, Dict, Optional
import uuid

app = Flask(__name__)

# In-memory storage (replace with a proper database in production)
health_records: Dict[str, Dict] = {}

class HealthRecord:
    def __init__(self, record_type: str, patient_id: str, timestamp: datetime = None):
        self.id = str(uuid.uuid4())
        self.record_type = record_type
        self.patient_id = patient_id
        self.timestamp = timestamp or datetime.now()

class LabResult(HealthRecord):
    def __init__(self, patient_id: str, value: float, description: str):
        super().__init__("lab_result", patient_id)
        self.value = value
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.record_type,
            "patient_id": self.patient_id,
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "description": self.description
        }

class Prescription(HealthRecord):
    def __init__(self, patient_id: str, dose: str, drug: str):
        super().__init__("prescription", patient_id)
        self.dose = dose
        self.drug = drug

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.record_type,
            "patient_id": self.patient_id,
            "timestamp": self.timestamp.isoformat(),
            "dose": self.dose,
            "drug": self.drug
        }

class AppointmentNote(HealthRecord):
    def __init__(self, patient_id: str, note: str):
        super().__init__("appointment_note", patient_id)
        self.note = note

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.record_type,
            "patient_id": self.patient_id,
            "timestamp": self.timestamp.isoformat(),
            "note": self.note
        }

class SelfMeasurement(HealthRecord):
    def __init__(self, patient_id: str, value: float, description: str):
        super().__init__("self_measurement", patient_id)
        self.value = value
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.record_type,
            "patient_id": self.patient_id,
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "description": self.description
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health-records', methods=['POST'])
def add_health_record():
    data = request.get_json()
    
    if not data or 'type' not in data or 'patient_id' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    record_type = data['type']
    patient_id = data['patient_id']
    
    try:
        if record_type == "lab_result":
            record = LabResult(
                patient_id=patient_id,
                value=float(data['value']),
                description=data['description']
            )
        elif record_type == "prescription":
            record = Prescription(
                patient_id=patient_id,
                dose=data['dose'],
                drug=data['drug']
            )
        elif record_type == "appointment_note":
            record = AppointmentNote(
                patient_id=patient_id,
                note=data['note']
            )
        elif record_type == "self_measurement":
            record = SelfMeasurement(
                patient_id=patient_id,
                value=float(data['value']),
                description=data['description']
            )
        else:
            return jsonify({"error": "Invalid record type"}), 400

        health_records[record.id] = record.to_dict()
        return jsonify(record.to_dict()), 201

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health-records', methods=['GET'])
def get_health_records():
    patient_id = request.args.get('patient_id')
    record_type = request.args.get('type')
    
    records = list(health_records.values())
    
    if patient_id:
        records = [r for r in records if r['patient_id'] == patient_id]
    if record_type:
        records = [r for r in records if r['type'] == record_type]
        
    return jsonify(records)

if __name__ == '__main__':
    app.run(debug=True)