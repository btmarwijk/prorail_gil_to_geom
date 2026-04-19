from fastapi import APIRouter, File, HTTPException, UploadFile
from services.upload_service import UploadService
from utils.excel_validation import is_valid_excel

# from sqlalchemy.orm import Session
# from core.database import get_db

router = APIRouter()


@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    valid_excel_extensions = {".xlsx", ".xls", ".xlsm"}

    # Validatie (houd dit kort in de router)
    if not any(file.filename.lower().endswith(ext) for ext in valid_excel_extensions):
        raise HTTPException(
            status_code=400, detail=f"Bestand {file.filename} is geen Excel."
        )
    contents = await file.read()
    if not is_valid_excel(contents):
        raise HTTPException(
            status_code=400, detail=f"Bestand {file.filename} is corrupt."
        )

    try:
        service = UploadService()
        upload_ids = service.process(excel_file=contents)

        return {
            "status": "success",
            "message": f"{len(upload_ids)} bestanden succesvol verwerkt.",
            "upload_ids": upload_ids,
        }
    except Exception as e:
        # db.rollback()  # Veiligheid boven alles
        raise HTTPException(status_code=500, detail=f"Fout tijdens verwerken: {str(e)}")
