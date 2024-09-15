from fastapi.testclient import TestClient
from .main import app
import uuid

client = TestClient(app)

file_id = str(uuid.uuid4())

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello oceanbridge-poc"}

def test_get_files():
    start_time = "2024-04-16T00:00:00Z"
    end_time = "2024-04-17T00:00:00Z"

    response = client.get("/V1/files", params={"updated_at_start_time": start_time, "updated_at_end_time": end_time})

    assert response.status_code == 200
    data = response.json()
    assert data["Status"] == "Success"

def test_get_file():
    file_id = "c24b1518-ccf6-46a7-ae1f-fbd0e7f90f2e"
    response = client.get(f"/V1/files/{file_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["Status"] == "Success"

def test_create_file():
    file_data = {
        "file_id": file_id,
        "file_upload_pending": True,
        "file_privacy_type_choice": str(uuid.uuid4()),
        "file_is_linked_to_table": "file_linked_table",
        "file_is_linked_to_id": str(uuid.uuid4()),
        "file_type_choice": str(uuid.uuid4()),
        "file_sub_type_choice": str(uuid.uuid4()),
        "file_size_kb": 0,
        "file_name": "file_name",
        "file_owner_entity_id": str(uuid.uuid4()),
        "file_uploaded_by_id": str(uuid.uuid4()),
        "file_uploaded_on": "2024-04-12T10:00:00Z",
        "file_replaces_file_id": str(uuid.uuid4()),
        "is_soft_deleted": True,
        "is_hard_deleted": True,
        "file_extension": "file_extension",
        "last_access_date": "2024-04-16T10:00:00Z",
        "last_checked_for_malware": "2024-04-16T10:00:00Z",
        "file_accessed_times" : 1,
        "SHA_256_hash": "asw3r!@$ds",
        "public_access_token_url_suffix": "token_url_suffix",
        "viewable_by_anyone_with_public_access_token": True,
        "is_data_pull_needed": False,
        "deleted_at" : None,
        "created_at": "2024-03-01T10:00:00Z",
        "updated_at": "2024-03-01T10:00:00Z"
    }

    response = client.post("/V1/files", json=file_data)

    assert response.status_code == 201
    assert response.json() == {"Status": "Success", "file_id": entity_id}


def test_update_file():
    file_id = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
    update_data = {
        "file_upload_pending": True,
        "file_privacy_type_choice": str(uuid.uuid4()),
        "file_is_linked_to_table": "updated_file_linked_table",
        "file_is_linked_to_id": str(uuid.uuid4()),
        "file_type_choice": str(uuid.uuid4()),
        "file_sub_type_choice": str(uuid.uuid4()),
        "file_size_kb": 0,
        "file_name": "updated_file_name",
        "file_owner_entity_id": str(uuid.uuid4()),
        "file_uploaded_by_id": str(uuid.uuid4()),
        "file_uploaded_on": "2024-04-16T10:00:00Z",
        "file_replaces_file_id": str(uuid.uuid4()),
        "is_soft_deleted": True,
        "is_hard_deleted": True,
        "file_extension": "updated_file_extension",
        "last_access_date": "2024-04-26T10:00:00Z",
        "last_checked_for_malware": "2024-04-26T10:00:00Z",
        "file_accessed_times" : 1,
        "SHA_256_hash": "updateasw3r!@$ds",
        "public_access_token_url_suffix": "update_token_url_suffix",
        "viewable_by_anyone_with_public_access_token": True,
        "is_data_pull_needed": False,
        "deleted_at" : None,
        "created_at": "2024-04-01T10:00:00Z",
        "updated_at": "2024-04-01T10:00:00Z"
    }

    response = client.patch(f"/V1/files/{file_id}", json=update_data)

    assert response.status_code == 202
    assert response.json() == {"Status": "Success", "success": True}




