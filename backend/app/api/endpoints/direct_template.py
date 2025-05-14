"""
Direct template download endpoint that bypasses caching
"""
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse, StreamingResponse
from pathlib import Path
import time
import io
import os

router = APIRouter()

@router.get("/reordered-exam-template")
def download_reordered_exam_template():
    """
    Direct download of the reordered exam template with no caching
    """
    try:
        # Directly use the reordered template file
        template_file = Path(__file__).parent.parent.parent.parent / "static" / "templates" / "exam_template_reordered.xlsx"
        print(f"Serving reordered template from: {template_file}")
        
        if not template_file.exists():
            raise HTTPException(status_code=404, detail="Reordered template file not found")
        
        # Return the file directly using FileResponse for better performance
        return FileResponse(
            path=template_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="exam_template_reordered.xlsx"
        )
    except Exception as e:
        print(f"Error serving reordered template: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error serving template: {str(e)}")

@router.get("/direct-exam-template")
def download_direct_exam_template():
    """
    Direct download of the exam template with no caching
    """
    try:
        # FORCE using the reordered template
        template_file = Path(__file__).parent.parent.parent.parent / "static" / "templates" / "exam_template_reordered.xlsx"
        print(f"Direct endpoint FORCE using reordered template at: {template_file}")
        
        # Verify the file exists and log its details
        if not template_file.exists():
            print(f"ERROR: Direct endpoint - Template file does not exist at {template_file}")
            
            # Only fall back to other templates if reordered template doesn't exist
            template_paths = [
                Path(__file__).parent.parent.parent.parent / "static" / "templates" / "exam_template.xlsx",
                Path(__file__).parent.parent.parent / "templates" / "exam_template.xlsx",
                Path(__file__).parent.parent.parent / "public" / "templates" / "exam_template.xlsx",
                Path(__file__).parent.parent.parent.parent / "output" / "updated_exam_template.xlsx"
            ]
        
            # Only search for fallback templates if the reordered template doesn't exist
            template_file = None
            for path in template_paths:
                if path.exists():
                    template_file = path
                    print(f"Direct endpoint using fallback template at: {template_file}")
                    break
        
        if not template_file:
            raise HTTPException(status_code=404, detail="Template file not found in any location")
        
        # Create timestamp for cache busting
        timestamp = int(time.time())
        
        # Set headers to prevent caching
        headers = {
            "Content-Disposition": f"attachment; filename=exam_template_{timestamp}.xlsx",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
            "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "-1",
            "X-Cache-Bust": str(timestamp)
        }
        
        # Read the file into memory and return it as a streaming response
        with open(template_file, "rb") as file:
            content = file.read()
        
        return StreamingResponse(
            io.BytesIO(content),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )
        
    except Exception as e:
        print(f"Error in direct template endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error serving template: {str(e)}")
