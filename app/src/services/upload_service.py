import time
from datetime import datetime

from models import Upload, User
from schemas.meta_spoorkabel_schema import MetaSpoorkabelCreate
from sqlalchemy.orm import Session
from utils.excel_reader import ExcelReader


class UploadService:
    def __init__(self, db: Session):
        self.db = db

    def process_upload(
        self, excel_reader: ExcelReader, file_name: str, current_user: User
    ) -> list[MetaSpoorkabelCreate]:
        """Reads metadata from ExcelReader, registers the upload in the database,

        and returns the Pydantic list ready for creation.
        """
        start_time = time.time()

        # 1. Extract metadata parsed by the ExcelReader
        tekeningnaam = excel_reader.tekeningnamen_str
        versie = getattr(excel_reader, "versie", None)

        # Pull dimensions from df shapes tracked in the reader
        aantal_kabels = (
            excel_reader._raw_shape[0] if hasattr(excel_reader, "_raw_shape") else 0
        )
        aantal_valide = (
            excel_reader._shape_without_empty[0]
            if hasattr(excel_reader, "_shape_without_empty")
            else 0
        )

        # Handle the Excel 'gedownload' datetime safely
        download_dt = None
        raw_download = getattr(excel_reader, "gedownload", None)
        if isinstance(raw_download, datetime):
            download_dt = raw_download
        elif isinstance(raw_download, str):
            try:
                download_dt = datetime.fromisoformat(raw_download)
            except ValueError:
                download_dt = None

        # Calculate pure execution time up to this point
        processing_time = f"{time.time() - start_time:.3f}s"

        # 2. Create the Upload DB entry
        upload_record = Upload(
            user_id=current_user.id,
            tekeningnaam=tekeningnaam,
            versie=versie,
            aantal_kabels=aantal_kabels,
            aantal_valide_kabels=aantal_valide,
            download=download_dt,
            username=current_user.email,  # Storing the plaintext email/username
            bestandnaam=file_name,
            processing_time=processing_time,
            success="SUCCESS",
            created_at=datetime.utcnow(),
        )

        self.db.add(upload_record)
        self.db.commit()
        self.db.refresh(upload_record)

        # 3. Fetch the Pydantic list from the reader
        pydantic_list = excel_reader.to_pydantic_create()

        # Inject the freshly generated Upload ID into the schemas
        for item in pydantic_list:
            item.upload_guid = upload_record.id

        return pydantic_list
