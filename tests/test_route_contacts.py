import sys
import os

from unittest.mock import MagicMock, patch
import pytest

sys.path.append(os.getcwd())
from src.database.models import User
from src.services.auth import auth_service
from src.conf.messages import NOT_FOUND

@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.confirmed_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]

def test_get_contacts_not_found(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == NOT_FOUND


def test_create_contact(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/contacts",
            json={
                "first_name": "Cristiano",
                "last_name": "Ronaldo",
                "email": "cr7@gmail.com",
                "phone": "123123123",
                "birthday": "1985-03-14"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["first_name"] == "Cristiano"
        assert data["last_name"] == "Ronaldo"
        assert data["email"] == "cr7@gmail.com"
        assert data["phone"] == "123123123"
        assert "id" in data

def test_get_contacts(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["first_name"] == "Cristiano"
        assert "id" in data[0]

def test_get_contact_by_id(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/by_id/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["first_name"] == "Cristiano"
        assert data["last_name"] == "Ronaldo"
        assert data["email"] == "cr7@gmail.com"
        assert data["phone"] == "123123123"
        assert "id" in data

def test_get_contact_by_id_not_found(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/by_id/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == NOT_FOUND

def test_get_contacts_by_fname(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/by_fname/cristi",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        print(data)
        assert data[0]["first_name"] == "Cristiano"
        assert data[0]["last_name"] == "Ronaldo"
        assert data[0]["email"] == "cr7@gmail.com"
        assert data[0]["phone"] == "123123123"

def test_get_contacts_by_fname_not_found(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/by_fname/putin_die_pls",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == NOT_FOUND
        
        
def test_get_contacts_by_lname(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/by_lname/ron",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        print(data)
        assert data[0]["first_name"] == "Cristiano"
        assert data[0]["last_name"] == "Ronaldo"
        assert data[0]["email"] == "cr7@gmail.com"
        assert data[0]["phone"] == "123123123"

def test_get_contacts_by_lname_not_found(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/by_lname/putin_die_pls",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == NOT_FOUND
        
def test_get_contacts_by_email(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/by_email/cr7",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        print(data)
        assert data[0]["first_name"] == "Cristiano"
        assert data[0]["last_name"] == "Ronaldo"
        assert data[0]["email"] == "cr7@gmail.com"
        assert data[0]["phone"] == "123123123"

def test_get_contacts_by_email_not_found(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/by_email/putin_die_pls@gmail.com",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == NOT_FOUND 

def test_update_contact(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/1",
            json={
                "first_name": "Artur",
                "last_name": "Ronaldo",
                "email": "cr7@gmail.com",
                "phone": "123123123",
                "birthday": "2023-03-15"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["first_name"] == "Artur"
        assert data["last_name"] == "Ronaldo"
        assert data["email"] == "cr7@gmail.com"
        assert data["phone"] == "123123123"


def test_update_contact_not_found(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/2",
            json={
                "first_name": "Artur",
                "last_name": "Ronaldo",
                "email": "cr7@gmail.com",
                "phone": "123123123",
                "birthday": "2023-03-15"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == NOT_FOUND
        
def test_get_contacts_with_birthday(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/birthday/",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        print(data)
        assert data[0]["first_name"] == "Artur"
        assert data[0]["last_name"] == "Ronaldo"
        assert data[0]["email"] == "cr7@gmail.com"
        assert data[0]["phone"] == "123123123"


def test_delete_contact(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text


def test_repeat_delete_contact(client, token):
    with patch.object(auth_service, 'redis_cache') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == NOT_FOUND