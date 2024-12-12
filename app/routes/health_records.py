import logging
from flask import Blueprint, request, jsonify, render_template
from redis.exceptions import RedisError
from app.models.health_records import LabResult, Prescription, AppointmentNote, SelfMeasurement
from app.services.redis_service import get_redis_client

logger = logging.getLogger(__name__)

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
        logger.error(f"Critical database error occurred: {str(e)}", exc_info=True)
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except KeyError as e:
        logger.debug(f"Missing required field during validation: {str(e)}")
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        logger.debug(f"Invalid value during validation: {str(e)}")
        return jsonify({"error": str(e)}), 400

@health_records_bp.route('/health-records', methods=['GET'])
def get_health_records():
    try:
        patient_id = request.args.get('patient_id')
        redis_client = get_redis_client()
        filtered_records = get_records_by_patient_id(redis_client, patient_id)  
        
        return jsonify(filtered_records)
    except RedisError as e:
        return jsonify({"error": f"Critical database error occurred: {str(e)}"}), 500

@health_records_bp.route('/health-records/<patient_id>', methods=['DELETE'])
def delete_patient_records(patient_id):
    try:
        redis_client = get_redis_client()
        filtered_records = get_records_by_patient_id(redis_client, patient_id)  
        
        if not filtered_records:
            return jsonify({"message": f"No records found for patient {patient_id}"}), 200
        
        for record in filtered_records:
            delete_record_by_id(redis_client, record["id"])

        return jsonify({
            "message": f"All health records for patient {patient_id} deleted successfully"
        }), 200
        
    except RedisError as e:
        return jsonify({"error": f"Critical database error occurred: {str(e)}"}), 500

def get_records_by_patient_id(redis_client, patient_id=None):
    record_ids = set()
    all_patient_keys = redis_client.keys("patient:*")
    for key in all_patient_keys:
        record_ids.update(redis_client.smembers(key))
    
    records = []
    for record_id in record_ids:
        record_id = record_id.decode('utf-8') if isinstance(record_id, bytes) else record_id
        record_data = redis_client.hgetall(f"health_record:{record_id}")
        if record_data:
            # Decode record data, handling both bytes and strings
            decoded_record = {}
            for k, v in record_data.items():
                key = k.decode('utf-8') if isinstance(k, bytes) else k
                value = v.decode('utf-8') if isinstance(v, bytes) else v
                decoded_record[key] = value
            
            records.append(decoded_record)
    
    if not patient_id:
        return records
    
    # Filter records in memory by patient ID
    filtered_records = [
        record for record in records 
        if record.get('patient_id') == patient_id
    ]
    
    return filtered_records

def delete_record_by_id(redis_client, record_id):
    record_id = record_id.decode('utf-8') if isinstance(record_id, bytes) else str(record_id)
    record_data = redis_client.hgetall(f"health_record:{record_id}")
    
    if not record_data:
        return False 
    
    decoded_record = {}
    for k, v in record_data.items():
        key = k.decode('utf-8') if isinstance(k, bytes) else k
        value = v.decode('utf-8') if isinstance(v, bytes) else v
        decoded_record[key] = value

    if 'type' in decoded_record:
        redis_client.srem(f"type:{decoded_record['type']}", record_id)
    
    if 'provider' in decoded_record:
        redis_client.srem(f"provider:{decoded_record['provider']}", record_id)
    
    if 'patient_id' in decoded_record:
        redis_client.srem(f"patient:{decoded_record['patient_id']}", record_id)
    
    redis_client.delete(f"health_record:{record_id}")
    
    return True
