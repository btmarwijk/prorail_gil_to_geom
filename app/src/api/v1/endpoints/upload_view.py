import os
import shutil

from core.database import get_db
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from models import User
from schemas.meta_spoorkabel_schema import MetaSpoorkabelCreate
from services.upload_service import UploadService
from sqlalchemy.orm import Session
from utils.excel_reader import ExcelReader

router = APIRouter(prefix="/upload", tags=["Uploads"])


class UploadView:
    """
    Controller handling HTTP operations for Excel uploads.
    Separates network/file concerns from core business logic.
    """

    def __init__(self, db: Session):
        self.db = db
        self.service = UploadService(db)
        self.temp_dir = "/tmp/uploads"

    def _validate_file_extension(self, filename: str) -> None:
        """Ensures the uploaded file is a valid Excel document."""
        if not (filename.endswith(".xlsx") or filename.endswith(".xls")):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Only .xlsx and .xls are supported.",
            )

    def _save_file_temporarily(self, file: UploadFile, path: str) -> None:
        """Buffers the in-memory uploaded file to local storage."""
        os.makedirs(self.temp_dir, exist_ok=True)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    def _get_acting_user(self) -> User:
        """Mock method to fetch the user. Replace this with your Auth mechanism."""
        user = self.db.query(User).first()
        if not user:
            raise HTTPException(
                status_code=404, detail="No user found to assign upload to."
            )
        return user

    def process_request(self, file: UploadFile) -> list[MetaSpoorkabelCreate]:
        """Main execution flow for mapping, parsing, and logging the upload."""
        self._validate_file_extension(file.filename)
        temp_file_path = os.path.join(self.temp_dir, file.filename)

        try:
            # 1. Store locally for openpyxl
            self._save_file_temporarily(file, temp_file_path)

            # 2. Extract Data & Identify User
            excel_reader = ExcelReader(file_path=temp_file_path)
            current_user = self._get_acting_user()

            # 3. Call Service Layer
            return self.service.process_upload(
                excel_reader=excel_reader,
                file_name=file.filename,
                current_user=current_user,
            )

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"File processing failed: {str(e)}"
            )

        finally:
            # Always clean up after yourself!
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


# --- Endpoint Mapping ---
# FastAPI needs a standard function to map the route,
# so we instantiate our OOP class inside the endpoint!
@router.post("/excel", response_model=list[MetaSpoorkabelCreate])
async def upload_excel_file(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    view = UploadView(db)
    return view.process_request(file)
