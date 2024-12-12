from flask import Flask, request, jsonify, render_template, render_template_string
from datetime import datetime
from typing import List, Dict, Optional
import uuid
import json
import redis
from redis.exceptions import RedisError

app = Flask(__name__)

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            "config.json not found. Please create a config file with Redis connection details."
        )
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in config.json")

# Load configuration and initialize Redis client
try:
    config = load_config()
    redis_config = config.get('redis', {})
    redis_client = redis.Redis(
        host=redis_config.get('host', 'localhost'),
        port=redis_config.get('port', 6379),
        db=redis_config.get('db', 0),
        username=redis_config.get('username'),
        password=redis_config.get('password'),
        ssl=redis_config.get('ssl', False),
        decode_responses=True,
        socket_timeout=redis_config.get('socket_timeout', 5),
        socket_connect_timeout=redis_config.get('socket_connect_timeout', 5),
        retry_on_timeout=redis_config.get('retry_on_timeout', True)
    )
except Exception as e:
    print(f"Error initializing Redis client: {str(e)}")
    raise

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

    def to_dict(self):
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

    def to_dict(self):
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

    def to_dict(self):
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

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.record_type,
            "patient_id": self.patient_id,
            "provider": self.provider,
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "description": self.description
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health-records', methods=['POST'])
def add_health_record():
    try:
        data = request.get_json()
        
        if not data or 'type' not in data or 'patient_id' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        record_type = data['type']
        patient_id = data['patient_id']
        provider = data.get('provider')
        
        if record_type == "lab_result":
            record = LabResult(
                patient_id=patient_id,
                value=float(data['value']),
                description=data['description'],
                provider=provider
            )
        elif record_type == "prescription":
            record = Prescription(
                patient_id=patient_id,
                dose=data['dose'],
                drug=data['drug'],
                provider=provider
            )
        elif record_type == "appointment_note":
            record = AppointmentNote(
                patient_id=patient_id,
                note=data['note'],
                provider=provider
            )
        elif record_type == "self_measurement":
            record = SelfMeasurement(
                patient_id=patient_id,
                value=float(data['value']),
                description=data['description'],
                provider=provider
            )
        else:
            return jsonify({"error": "Invalid record type"}), 400

        record_dict = record.to_dict()
        redis_client.hset(
            f"health_record:{record.id}",
            mapping=record_dict
        )
        
        redis_client.sadd(f"patient:{patient_id}", record.id)
        redis_client.sadd(f"type:{record_type}", record.id)
        if provider:
            redis_client.sadd(f"provider:{provider}", record.id)
        
        return jsonify(record_dict), 201

    except RedisError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health-records', methods=['GET'])
def get_health_records():
    try:
        patient_id = request.args.get('patient_id')
        record_type = request.args.get('type')
        provider = request.args.get('provider')
        
        record_ids = set()
        filter_sets = []
        
        if patient_id:
            filter_sets.append(redis_client.smembers(f"patient:{patient_id}"))
        if record_type:
            filter_sets.append(redis_client.smembers(f"type:{record_type}"))
        if provider:
            filter_sets.append(redis_client.smembers(f"provider:{provider}"))
        
        if filter_sets:
            record_ids = set.intersection(*filter_sets) if len(filter_sets) > 1 else filter_sets[0]
        else:
            all_patient_keys = redis_client.keys("patient:*")
            for key in all_patient_keys:
                record_ids.update(redis_client.smembers(key))
        
        records = []
        for record_id in record_ids:
            record_data = redis_client.hgetall(f"health_record:{record_id}")
            if record_data:
                records.append(record_data)
        
        return jsonify(records)

    except RedisError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)