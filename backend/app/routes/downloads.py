"""
Direct download routes for files
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import os

router = APIRouter()

@router.get("/exam-template")
async def download_exam_template():
    """
    Direct download for the exam template
    """
    try:
        # First try the template in the static/templates directory
        template_path = Path("/app/static/templates/exam_template_reordered.xlsx")
        
        # If not found, try the root static directory
        if not template_path.exists():
            template_path = Path("/app/static/exam_template_reordered.xlsx")
            
        # If still not found, return an error
        if not template_path.exists():
            raise HTTPException(status_code=404, detail="Template file not found")
        
        # Log the file details
        file_size = os.path.getsize(template_path)
        print(f"Serving exam template from {template_path}, size: {file_size} bytes")
        
        # Return the file as a download
        return FileResponse(
            path=template_path,
            filename="exam_template_reordered.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        print(f"Error serving exam template: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error serving template: {str(e)}")
