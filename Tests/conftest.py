import pytest
from app import create_app
from app.services.redis_service import get_redis_client
import fakeredis

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create the app with test config
    app = create_app()
    app.config.update({
        'TESTING': True,
        'redis': {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        }
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def redis_mock(monkeypatch):
    """Replace Redis with fakeredis for testing."""
    fake_redis = fakeredis.FakeStrictRedis(decode_responses=True)
    monkeypatch.setattr('app.services.redis_service.redis_client', fake_redis)
    return fake_redis