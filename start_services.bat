@echo off
echo Starting Exam Planning System...

echo Starting Docker services...
docker-compose up -d

echo Starting frontend...
cd frontend
start cmd /k npm start

echo Services are starting. Please wait a moment before accessing:
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
