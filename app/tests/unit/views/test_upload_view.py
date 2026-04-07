from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

# Adjust these imports to match your project's file structure
from main import app  # Assuming your FastAPI app is initialized here
from schemas.meta_spoorkabel_schema import MetaSpoorkabelCreate

client = TestClient(app)


@pytest.fixture
def mock_upload_service():
    """Fixtures are a great way to clean up setup/mocking code."""
    with patch("upload_view.UploadService") as mock:
        yield mock


@pytest.fixture
def mock_excel_reader():
    """Mock the heavy openpyxl reader so we don't need real files."""
    with patch("upload_view.ExcelReader") as mock:
        yield mock


## --- Test Cases ---


def test_upload_excel_success(mock_upload_service, mock_excel_reader):
    """GIVEN a valid .xlsx file

    WHEN the user uploads it
    THEN it should return 200 and the list of mapped cables.
    """
    # 1. Arrange: Create a fake return value for our service
    mock_service_instance = mock_upload_service.return_value
    mock_service_instance.process_upload.return_value = [
        MetaSpoorkabelCreate(
            upload_guid=1,
            tekeningnaam="Drawing_A",
            geocodenaam="Geo_1",
            versie="1.0",
        )
    ]

    # Mock the reader's properties if the service relies on them directly
    mock_reader_instance = mock_excel_reader.return_value
    mock_reader_instance.tekeningnamen_str = "Drawing_A"

    # 2. Act: Simulate sending a file over HTTP
    fake_file_content = b"fake excel file binary data"
    response = client.post(
        "/upload/excel",
        files={
            "file": (
                "test_file.xlsx",
                fake_file_content,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )

    # 3. Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["tekeningnaam"] == "Drawing_A"


def test_upload_invalid_extension():
    """GIVEN a file with an invalid extension (e.g., .txt)

    WHEN the user attempts to upload it
    THEN it should be blocked with a 400 Bad Request before processing.
    """
    # Act
    response = client.post(
        "/upload/excel",
        files={"file": ("malicious_script.txt", b"print('hello')", "text/plain")},
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Only .xlsx and .xls are supported" in response.json()["detail"]


def test_upload_processing_failure(mock_upload_service, mock_excel_reader):
    """GIVEN a situation where processing throws an unexpected error

    WHEN the user uploads a valid file
    THEN it should catch it and return a 500 Server Error safely.
    """
    # Arrange: Force the service to blow up
    mock_service_instance = mock_upload_service.return_value
    mock_service_instance.process_upload.side_effect = Exception("Corrupt sheet!")

    # Act
    response = client.post(
        "/upload/excel",
        files={
            "file": (
                "broken_file.xlsx",
                b"corrupt data",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )

    # Assert
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "File processing failed" in response.json()["detail"]
