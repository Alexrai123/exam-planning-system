from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routes import users, courses, groups, rooms, exams, auth, exports, professors, external_data, faculties, downloads, specializations, group_leaders
from .api.api import api_router
from .core.config import settings
from .core.cors import setup_cors

app = FastAPI(
    title="Sistem informatic pentru planificarea examenelor și a colocviilor",
    description="Backend API pentru planificarea și gestionarea examenelor",
    version="1.0.0"
)

# Setup CORS using the configuration from core.cors
setup_cors(app)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Authentication"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["Users"])
app.include_router(courses.router, prefix=settings.API_V1_STR, tags=["Courses"])
app.include_router(groups.router, prefix=settings.API_V1_STR, tags=["Groups"])
app.include_router(rooms.router, prefix=settings.API_V1_STR, tags=["Rooms"])
app.include_router(exams.router, prefix=settings.API_V1_STR, tags=["Exams"])
app.include_router(exports.router, prefix=settings.API_V1_STR, tags=["Exports"])
app.include_router(professors.router, prefix=settings.API_V1_STR, tags=["Professors"])
app.include_router(faculties.router, prefix=settings.API_V1_STR, tags=["Faculties"])
app.include_router(specializations.router, prefix=settings.API_V1_STR, tags=["Specializations"])
app.include_router(external_data.router, prefix=f"{settings.API_V1_STR}/external-data", tags=["External Data"])
app.include_router(downloads.router, prefix=f"{settings.API_V1_STR}/downloads", tags=["Downloads"])
app.include_router(group_leaders.router, prefix=settings.API_V1_STR, tags=["Group Leaders"])

# Include API router for templates
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files directory
app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent / "static"), name="static")

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Exam Planning System API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
