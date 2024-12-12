from flask import Blueprint, request, jsonify, render_template
from redis.exceptions import RedisError
from app.models.health_records import LabResult, Prescription, AppointmentNote, SelfMeasurement
from app.services.redis_service import get_redis_client

health_records_bp = Blueprint('health_records', __name__)

@health_records_bp.route('/')
def home():
    return render_template('index.html')

@health_records_bp.route('/health-records', methods=['POST'])
def add_health_record():
    try:
        data = request.get_json()
        
        if not data or 'type' not in data or 'patient_id' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        record_type = data['type']
        patient_id = data['patient_id']
        provider = data.get('provider')
        
        record = None
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

        redis_client = get_redis_client()
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

@health_records_bp.route('/health-records', methods=['GET'])
def get_health_records():
    try:
        patient_id = request.args.get('patient_id')
        record_type = request.args.get('type')
        provider = request.args.get('provider')
        
        redis_client = get_redis_client()
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