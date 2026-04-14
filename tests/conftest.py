import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

@pytest.fixture(autouse=True)
def reset_activities():
    # Deep copy the original activities dict for isolation
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))

@pytest.fixture
def client():
    return TestClient(app)
