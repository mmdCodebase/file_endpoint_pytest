from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from app.models.user import Authentication, AuthenticationRecoveryMFA, AuthenticationToken

client = TestClient(app)

# def test_root():
#     response = client.get("/api/healthchecker")
#     assert response.status_code == 200
#     assert response.json() == {"message": "The API is LIVE!!"}

def test_get_updated_users():
    # Mock the database session and query method
    db_mock = MagicMock(spec=Session)

    # Define the start and end times for the query
    start_time = "2024-04-16T00:00:00Z"
    end_time = "2024-04-17T00:00:00Z"

    # Mock the query method to return a list of Authentication entities with entity_id attributes
    updated_users_data = [
        Authentication(entity_id="123e4567-e89b-12d3-a456-426614174000"),
        Authentication(entity_id="c456e321-e89b-12d3-a456-426614174001"),
    ]
    db_mock.query().filter().all.return_value = updated_users_data

    response = client.get("/V1/authentication/user", params={"updated_start_time": start_time, "updated_end_time": end_time})

    assert response.status_code == 200
    assert response.json() == {"Status": "Success", "updated_users": ["123e4567-e89b-12d3-a456-426614174000", "c456e321-e89b-12d3-a456-426614174001"]}
    
def test_get_user():
    # Mock the database session and queries
    db_mock = MagicMock(spec=Session)
    entity_id = "123e4567-e89b-12d3-a456-426614174000"
    
    # Mock the query method to return user data
    db_mock.query.return_value.filter.return_value.first.return_value = Authentication(
        entity_id=entity_id,
        contact_id="e210g987-e89b-12d3-a456-426614174003",
        username="john.doe",
        user_secret_server_salt="serversalt",
        plaintext_password="plaintextpassword",
        hashed_password="hashedpassword",
        is_active=True,
        password_updated_on="2024-03-12T10:00:00Z",
        ottp_secret_key="ottpsecretkey",
        failed_login_attempts_since_last_login="failedloginlast",
        account_status_choice="ae34ee56-e89b-12d3-a456-426614174000",
        two_factor_authentication_enabled=True,
        password_recovery_choice="d789f654-e89b-12d3-a456-426614174002",
        second_factor_authentication_choice="e210g987-e89b-12d3-a456-426614174003",
        account_lock_expiry="2024-04-12T10:00:00Z",
        last_password_reset="2024-03-01T10:00:00Z",
        force_password_change=False,
        user_is_super_admin = False,
        updated_at="2024-04-13T10:00:00Z"
    )

    # Mock the query method to return recovery data
    db_mock.query.return_value.filter.return_value.all.return_value = [
        AuthenticationRecoveryMFA(
            recovery_id="1",
            entity_id=entity_id,
            recovery_type_choice="fs34s-fsfil4",
            recovery_key="recovery_key_1",
            recovery_value="recovery_value_1"
        ),
        AuthenticationRecoveryMFA(
            recovery_id="2",
            entity_id=entity_id,
            recovery_type_choice="af34s-affi5",
            recovery_key="recovery_key_2",
            recovery_value="recovery_value_2"
        )
    ]

    # Mock the query method to return token data
    db_mock.query.return_value.filter.return_value.all.return_value = [
        AuthenticationToken(
            authentication_token_id="1",
            entity_id=entity_id,
            ip_address="127.0.0.1",
            browser="Chrome",
            os="Windows",
            device_id="device_1",
            is_active=True,
            access_token="access_token_1",
            refresh_token="refresh_token_1",
            access_token_expired_at="2024-05-01T00:00:00Z",
            refresh_token_expired_at="2024-06-01T00:00:00Z",
            deleted_at=null,
            created_at="2024-03-13T10:00:00Z",
            updated_at="2024-03-13T10:00:00Z",
            last_login_date="2024-03-13T10:00:00Z"
        ),
        AuthenticationToken(
            authentication_token_id="2",
            entity_id=entity_id,
            ip_address="127.0.0.1",
            browser="Firefox",
            os="Linux",
            device_id="device_2",
            is_active=True,
            access_token="access_token_2",
            refresh_token="refresh_token_2",
            access_token_expired_at="2024-05-01T00:00:00Z",
            refresh_token_expired_at="2024-06-01T00:00:00Z",
            deleted_at=null,
            created_at="2024-03-13T10:00:00Z",
            updated_at="2024-03-13T10:00:00Z",
            last_login_date="2024-03-13T10:00:00Z"
        )
    ]

    response = client.get(f"/V1/authentication/user/{entity_id}")

    assert response.status_code == 200
    assert response.json() == {
        "Status": "Success",
        "user_data": {
            "entity_id": entity_id,
            "contact_id": "e210g987-e89b-12d3-a456-426614174003",
            "username": "john.doe",
            "user_secret_server_salt": "serversalt",
            "plaintext_password": "plaintextpassword",
            "hashed_password": "hashedpassword",
            "is_active": True,
            "password_updated_on": "2024-03-12T10:00:00Z",
            "ottp_secret_key": "ottpsecretkey",
            "failed_login_attempts_since_last_login": "failedloginlast",
            "account_status_choice": "ae34ee56-e89b-12d3-a456-426614174000",
            "two_factor_authentication_enabled": True,
            "password_recovery_choice": "d789f654-e89b-12d3-a456-426614174002",
            "second_factor_authentication_choice": "e210g987-e89b-12d3-a456-426614174003",
            "account_lock_expiry": "2024-04-12T10:00:00Z",
            "last_password_reset": "2024-03-01T10:00:00Z",
            "force_password_change": False,
            "user_is_super_admin" : False,
            "updated_at": "2024-04-13T10:00:00Z"
        },
        "recovery_data": [
            {
                "recovery_id": "1",
                "entity_id": entity_id,
                "recovery_type_choice": "fs34s-fsfil4",
                "recovery_key": "recovery_key_1",
                "recovery_value": "recovery_value_1"
            },
            {
                "recovery_id": "2",
                "entity_id": entity_id,
                "recovery_type_choice": "af34s-affi5",
                "recovery_key": "recovery_key_2",
                "recovery_value": "recovery_value_2"
            }
        ],
        "auth_tokens": [
            {
                "authentication_token_id": "1",
                "entity_id": entity_id,
                "ip_address": "127.0.0.1",
                "browser": "Chrome",
                "os": "Windows",
                "device_id": "device_1",
                "is_active": True,
                "access_token": "access_token_1",
                "refresh_token": "refresh_token_1",
                "access_token_expired_at": "2024-05-01T00:00:00Z",
                "refresh_token_expired_at": "2024-06-01T00:00:00Z",
                "deleted_at": null,
                "created_at": "2024-03-13T10:00:00Z",
                "updated_at": "2024-03-13T10:00:00Z",
                "last_login_date": "2024-03-13T10:00:00Z"
            },
            {
                "authentication_token_id": "2",
                "entity_id": entity_id,
                "ip_address": "127.0.0.1",
                "browser": "Firefox",
                "os": "Linux",
                "device_id": "device_2",
                "is_active": True,
                "access_token": "access_token_2",
                "refresh_token": "refresh_token_2",
                "access_token_expired_at": "2024-05-01T00:00:00Z",
                "refresh_token_expired_at": "2024-06-01T00:00:00Z",
                "deleted_at": null,
                "created_at": "2024-03-13T10:00:00Z",
                "updated_at": "2024-03-13T10:00:00Z",
                "last_login_date": "2024-03-13T10:00:00Z"
            }
        ]
    }


def test_create_authentication_user():
    # Mock the database session and add method
    db_mock = MagicMock(spec=Session)
    
    # Define the authentication user data
    authentication_user_data = {
        "contact_id": "e210g987-e89b-12d3-a456-426614174003",
        "username": "john.doe",
        "user_secret_server_salt": "serversalt",
        "plaintext_password": "plaintextpassword",
        "hashed_password": "hashedpassword",
        "is_active": True,
        "password_updated_on": "2024-03-12T10:00:00Z",
        "ottp_secret_key": "ottpsecretkey",
        "failed_login_attempts_since_last_login": "failedloginlast",
        "account_status_choice": "ae34ee56-e89b-12d3-a456-426614174000",
        "two_factor_authentication_enabled": True,
        "password_recovery_choice": "d789f654-e89b-12d3-a456-426614174002",
        "second_factor_authentication_choice": "e210g987-e89b-12d3-a456-426614174003",
        "account_lock_expiry": "2024-04-12T10:00:00Z",
        "last_password_reset": "2024-03-01T10:00:00Z",
        "force_password_change": False,
        "user_is_super_admin" : False,
        "updated_at": "2024-04-13T10:00:00Z"
    }

    # Mock the add method to return the authentication user entity with a predefined entity_id
    db_mock.add.return_value = None
    db_mock.commit.return_value = None
    db_mock.refresh.return_value = None
    db_mock.add.return_value.entity_id = "1"

    response = client.post("/V1/authentication/user", json=authentication_user_data)

    assert response.status_code == 201
    assert response.json() == {"Status": "Success", "authentication_user_id": "1"}


def test_update_authentication_user():
    # Mock the database session and query method
    db_mock = MagicMock(spec=Session)

    # Define the entity_id for the user to be updated
    entity_id = "1"

    # Define the update data for the user
    update_data = {
        "contact_id": "e210g987-e89b-12d3-a456-426614174003",
        "username": "john.doe",
        "user_secret_server_salt": "serversalt",
        "plaintext_password": "plaintextpassword",
        "hashed_password": "hashedpassword",
        "is_active": True,
        "password_updated_on": "2024-03-12T10:00:00Z",
        "ottp_secret_key": "ottpsecretkey",
        "failed_login_attempts_since_last_login": "failedloginlast",
        "account_status_choice": "ae34ee56-e89b-12d3-a456-426614174000",
        "two_factor_authentication_enabled": True,
        "password_recovery_choice": "d789f654-e89b-12d3-a456-426614174002",
        "second_factor_authentication_choice": "e210g987-e89b-12d3-a456-426614174003",
        "account_lock_expiry": "2024-04-12T10:00:00Z",
        "last_password_reset": "2024-03-01T10:00:00Z",
        "force_password_change": False,
        "user_is_super_admin" : False,
        "updated_at": "2024-04-13T10:00:00Z"
    }

    # Mock the query method to return the authentication user entity with the predefined entity_id
    db_mock.query.return_value.filter.return_value.first.return_value = Authentication(entity_id=entity_id)

    response = client.patch(f"/V1/authentication/user/{entity_id}", json=update_data)

    assert response.status_code == 202
    assert response.json() == {"Status": "Success", "success": True}


def test_create_authentication_token():
    # Mock the database session and query method
    db_mock = MagicMock(spec=Session)

    # Define the data for the new authentication token
    token_data = {
        "authentication_token_id": "1",
        "entity_id": entity_id,
        "ip_address": "127.0.0.1",
        "browser": "Chrome",
        "os": "Windows",
        "device_id": "device_1",
        "is_active": True,
        "access_token": "access_token_1",
        "refresh_token": "refresh_token_1",
        "access_token_expired_at": "2024-05-01T00:00:00Z",
        "refresh_token_expired_at": "2024-06-01T00:00:00Z",
        "deleted_at": null,
        "created_at": "2024-03-13T10:00:00Z",
        "updated_at": "2024-03-13T10:00:00Z",
        "last_login_date": "2024-03-13T10:00:00Z"
    }

    # Mock the add method to return the authentication token entity with the predefined token
    db_mock.add.return_value = AuthenticationToken(**token_data)

    response = client.post("/V1/authentication/token", json=token_data)

    assert response.status_code == 200
    assert response.json() == {"Status": "Success", "authentication_token_id": "1"}


def test_update_authentication_token():
    # Mock the database session and query method
    db_mock = MagicMock(spec=Session)

    # Define the data for the updated authentication token
    token_id = "1"
    updated_data = {
        "authentication_token_id": "2"
    }

    # Mock the query method to return the authentication token entity with the predefined token ID
    authentication_token_db_mock = AuthenticationToken(authentication_token_id=token_id, token="oldtoken")
    db_mock.query().filter().first.return_value = authentication_token_db_mock

    response = client.patch(f"/V1/authentication/token/{token_id}", json=updated_data)

    assert response.status_code == 200
    assert response.json() == {"Status": "Success", "success": True}

    # Verify that the token was updated in the database
    assert authentication_token_db_mock.authentication_token_id == "2"


