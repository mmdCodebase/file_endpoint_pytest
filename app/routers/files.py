from fastapi import APIRouter, Query, Depends, HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session
from db.database import get_db
from models.file import File, FileCreate, FileUpdate

router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_files(updated_at_start_time: datetime = Query(None), updated_at_end_time: datetime = Query(None), db: Session = Depends(get_db)):
    """
    Endpoint to fetch files based on provided date range.
    """
    if updated_at_start_time is None or updated_at_end_time is None:
        return {"error": "Both updated_at_start_time and updated_at_end_time query parameters are required."}
    
    files = db.query(File).filter(File.updated_at > updated_at_start_time, File.updated_at < updated_at_end_time).all()
    return {"Status":"Success", "files": [file.file_id for file in files]}

@router.get("/{file_id}", status_code=status.HTTP_200_OK)
async def get_file(file_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to fetch file data based on provided file ID.
    """
    file_data = db.query(File).filter(File.file_id == file_id).first()
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")
    return {"Status": "Success", "file_data": file_data}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_file(file_data: FileCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new file record in the database.
    """
    file_db = File(**file_data.dict())
    db.add(file_db)
    db.commit()
    db.refresh(file_db)
    return {"Status":"Success", "file_id": file_db.file_id}

@router.patch("/{file_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_file(file_id: str, file_data: FileUpdate, db: Session = Depends(get_db)):
    """
    Endpoint to update file data based on provided file ID.
    """
    file_db = db.query(File).filter(File.file_id == file_id).first()
    if not file_db:
        raise HTTPException(status_code=404, detail="File not found")
    
    for key, value in file_data.items():
        setattr(file_db, key, value)
    
    try:
        db.commit()
        return {"Status": "Success", "success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update file data") from e




