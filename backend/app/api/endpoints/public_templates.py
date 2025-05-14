"""
Public API endpoints for Excel templates (no authentication required)
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Optional
from pathlib import Path
import io
import time
import os

from app.templates import generate_course_template, generate_exam_template, generate_student_template

router = APIRouter()

@router.get("/course")
def download_course_template_public():
    """
    Download Excel template for course data (public endpoint)
    """
    try:
        print("Generating public course template")
        output = generate_course_template()
        
        # Add CORS headers
        headers = {
            "Content-Disposition": "attachment; filename=course_template.xlsx",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type"
        }
        
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )
    except Exception as e:
        print(f"Error generating public course template: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating template: {str(e)}")

@router.get("/exam")
def download_exam_template_public():
    """
    Download Excel template for exam data (public endpoint)
    """
    try:
        # FORCE using the reordered template - no fallbacks
        template_file = Path(__file__).parent.parent.parent.parent / "static" / "templates" / "exam_template_reordered.xlsx"
        print(f"FORCE using reordered template at: {template_file}")
        
        # Verify the file exists and log its details
        if not template_file.exists():
            print(f"ERROR: Template file does not exist at {template_file}")
            raise FileNotFoundError(f"Template file not found at {template_file}")
            
        # Log file size and modification time for debugging
        file_size = template_file.stat().st_size
        mod_time = template_file.stat().st_mtime
        print(f"Template file details: Size={file_size} bytes, Last Modified={mod_time}")
        
        # Template file is already set above
        
        if template_file:
            # Add timestamp to filename to prevent caching
            timestamp = int(time.time())
            headers = {
                "Content-Disposition": f"attachment; filename=exam_template_{timestamp}.xlsx",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Authorization, Content-Type",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
            
            # Return the static file
            with open(template_file, "rb") as f:
                content = f.read()
            
            return StreamingResponse(
                io.BytesIO(content),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers=headers
            )
        
        # If no static file is found, generate one dynamically
        print("Generating public exam template dynamically")
        output = generate_exam_template()
        
        # Add simple headers
        headers = {
            "Content-Disposition": "attachment; filename=exam_template.xlsx",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
        
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )
    except Exception as e:
        print(f"Error generating public exam template: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating template: {str(e)}")

@router.get("/student")
def download_student_template_public():
    """
    Download Excel template for student data (public endpoint)
    """
    try:
        print("Generating public student template")
        output = generate_student_template()
        
        # Add CORS headers
        headers = {
            "Content-Disposition": "attachment; filename=student_template.xlsx",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type"
        }
        
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )
    except Exception as e:
        print(f"Error generating public student template: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating template: {str(e)}")
