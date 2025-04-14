from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routes import users, courses, groups, rooms, exams, auth, exports, professors, external_data, faculties
from .core.config import settings

app = FastAPI(
    title="Sistem informatic pentru planificarea examenelor și a colocviilor",
    description="Backend API pentru planificarea și gestionarea examenelor",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(external_data.router, prefix=f"{settings.API_V1_STR}/external-data", tags=["External Data"])

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Exam Planning System API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
