from typing import Annotated
from fastapi import Depends
from starlette import status
from starlette.testclient import TestClient
from ..main import app
from .utils import *
from ..routers.auth import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
user_dependency = Annotated[dict, Depends(get_current_user)]

client = TestClient(app)


def test_create_subject(test_subject):
    request_data = {
        "name": "Physics"
    }
    response = client.post('/admin/subjects', json=request_data)
    db = TestingSessionLocal()
    model = db.query(Subject).filter(Subject.id == 2).first()
    assert response.status_code == status.HTTP_201_CREATED
    assert model.name == request_data.get('name')
