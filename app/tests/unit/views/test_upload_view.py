import io

import pandas as pd
import pytest
from httpx import ASGITransport, AsyncClient
from main import app


@pytest.mark.asyncio
async def test_upload_excel_success():
    # 1. Create a dummy DataFrame and convert to Excel bytes
    df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [25, 30]})
    excel_buffer = io.BytesIO()

    # Ensure openpyxl is installed for this to work
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    excel_buffer.seek(0)

    # 2. Setup the AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as ac:
        # 3. Prepare the file
        files = {
            "file": (
                "test.xlsx",
                excel_buffer,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        }

        # 4. Perform the POST request using the FULL path from your docs
        # Path: /api/v1/uploads/upload-excel
        response = await ac.post("/api/v1/uploads/upload-excel", files=files)

    # 5. Assertions
    assert response.status_code == 200
    if response.status_code == 422:
        print(response.json())
    data = response.json()
    assert data["filename"] == "test.xlsx"
    assert data["rows"] == 2
    assert data["data"][0]["Name"] == "Alice"


@pytest.mark.asyncio
async def test_upload_no_file():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as ac:
        # Correct path here as well
        response = await ac.post("/api/v1/uploads/upload-excel")

    assert response.status_code == 422
