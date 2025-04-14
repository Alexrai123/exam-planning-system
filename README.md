# Exam Planning System

A comprehensive web application for planning and managing university exams, built with FastAPI, PostgreSQL, and React.

## Project Overview

The Exam Planning System is designed to help universities manage and schedule exams efficiently. It provides a comprehensive solution for professors, students, and administrative staff to coordinate exam scheduling.

### Key Features

- **User Authentication**: JWT token-based authentication with role-based access control
- **Exam Scheduling**: Create, view, and manage exams with status tracking
- **Group Leader Functionality**: Student representatives can propose exam dates
- **Calendar View**: Visualize exam schedules in an interactive calendar
- **Room Management**: Track room availability and capacity
- **Course Management**: Organize courses and their associated professors

## Project Structure

- **backend/**: FastAPI backend code
- **frontend/**: React frontend code
- **sql/**: SQL scripts for database management
- **scripts/**: PowerShell and Python scripts for automation
- **backups/**: Database backup files
- **docs_final/**: Comprehensive documentation
- **diagrams/**: System architecture diagrams

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Frontend**: React
- **Containerization**: Docker
- **Documentation**: Sphinx with Napoleon extension

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git
- Node.js and npm (for frontend development)
- Python 3.8+ (for local development)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/exam-planning-system.git
   cd exam-planning-system
   ```

2. Start the Docker containers:
   ```
   docker-compose up -d
   ```

3. Start the frontend development server:
   ```
   cd frontend
   npm install
   npm start
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Documentation

Comprehensive documentation is available in the `docs_final` directory. Open `docs_final/index.html` in your browser to view the documentation, which includes:

- System architecture
- API reference
- Data models
- Database schema
- Deployment instructions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Alex - Project creator and maintainer
