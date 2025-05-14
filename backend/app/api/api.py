"""
Main API router
"""
from fastapi import APIRouter

from app.api.endpoints import templates, test, public_templates, imports, public_imports, direct_template

api_router = APIRouter()

# Include template endpoints
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])

# Include test endpoints
api_router.include_router(test.router, prefix="/test", tags=["test"])

# Include public template endpoints (no authentication required)
api_router.include_router(public_templates.router, prefix="/public/templates", tags=["public"])

# Include import endpoints
api_router.include_router(imports.router, prefix="/imports", tags=["imports"])

# Include public import endpoints (no authentication required)
api_router.include_router(public_imports.router, prefix="/public/imports", tags=["public"])

# Include direct template endpoints (no authentication required)
api_router.include_router(direct_template.router, prefix="/direct-template", tags=["public"])

# Add other routers here as needed
