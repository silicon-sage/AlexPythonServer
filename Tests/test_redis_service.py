import pytest
from app.services.redis_service import init_redis_client, get_redis_client

def test_redis_initialization(app):
    redis_client = init_redis_client(app)
    assert redis_client is not None
    assert get_redis_client() is redis_client

def test_redis_operations(redis_mock):
    redis_mock.set('test_key', 'test_value')
    assert redis_mock.get('test_key') == 'test_value'
    
    redis_mock.hset('test_hash', 'field1', 'value1')
    assert redis_mock.hget('test_hash', 'field1') == 'value1'
    
    redis_mock.sadd('test_set', 'member1')
    assert redis_mock.smembers('test_set') == {'member1'}