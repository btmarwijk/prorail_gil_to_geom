from fastapi import APIRouter, File, UploadFile
from services.upload_service import UploadProcessor

router = APIRouter()
processor = UploadProcessor(preview_rows=10)


@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    contents = await file.read()
    excel_reader = processor.process(contents)
    parsed_excel = excel_reader.to_pydantic_create()
    return [parsed.model_dump(by_alias=True) for parsed in parsed_excel]
