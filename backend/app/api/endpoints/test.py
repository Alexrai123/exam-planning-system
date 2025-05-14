"""
Test endpoints for debugging
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/ping")
def ping():
    """
    Simple ping endpoint for testing connectivity
    """
    return JSONResponse(
        content={"message": "pong"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type"
        }
    )

@router.get("/template-test")
def template_test():
    """
    Test endpoint for template download without authentication
    """
    return JSONResponse(
        content={"message": "Template API is accessible"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type"
        }
    )
