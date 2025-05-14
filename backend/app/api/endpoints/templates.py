"""
API endpoints for Excel templates
"""
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from typing import List, Optional
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User, UserRole
from app.templates import generate_course_template, generate_exam_template, generate_student_template

router = APIRouter()

@router.get("/course")
def download_course_template(
    current_user: User = Depends(deps.get_current_user_with_roles([UserRole.SECRETARIAT, UserRole.ADMIN]))
):
    """
    Download Excel template for course data
    """
    try:
        print(f"Generating course template for user: {current_user.email}")
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
        print(f"Error generating course template: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating template: {str(e)}")


@router.get("/exam")
def download_exam_template(
    current_user: User = Depends(deps.get_current_user_with_roles([UserRole.SECRETARIAT, UserRole.ADMIN]))
):
    """
    Download Excel template for exam data
    """
    try:
        print(f"Generating exam template for user: {current_user.email}")
        
        # Use the reordered template from the static templates directory
        from pathlib import Path
        import io
        
        template_file = Path(__file__).parent.parent.parent.parent / "static" / "templates" / "exam_template_reordered.xlsx"
        print(f"Authenticated endpoint using reordered template at: {template_file}")
        
        # Check if the reordered template exists
        if template_file.exists():
            # Read the file directly instead of generating it
            with open(template_file, "rb") as f:
                content = f.read()
            output = io.BytesIO(content)
        else:
            # Fall back to generating the template
            print("Reordered template not found, generating dynamically")
            output = generate_exam_template()
        
        # Add CORS headers
        headers = {
            "Content-Disposition": "attachment; filename=exam_template.xlsx",
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
        print(f"Error generating exam template: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating template: {str(e)}")

@router.get("/student")
def download_student_template(
    current_user: User = Depends(deps.get_current_user_with_roles([UserRole.SECRETARIAT, UserRole.ADMIN]))
):
    """
    Download Excel template for student data
    """
    try:
        print(f"Generating student template for user: {current_user.email}")
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
        print(f"Error generating student template: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating template: {str(e)}")

