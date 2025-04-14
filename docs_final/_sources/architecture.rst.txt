Architecture
============

System Architecture
------------------

The Exam Planning System follows a modern three-tier architecture:

.. code-block:: text

    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │   Frontend  │     │   Backend   │     │  Database   │
    │    (React)  │◄───►│  (FastAPI)  │◄───►│ (PostgreSQL)│
    └─────────────┘     └─────────────┘     └─────────────┘

Each component runs in its own environment:

* **Frontend**: React application running on port 3000
* **Backend**: FastAPI application running in Docker container on port 8000
* **Database**: PostgreSQL running in Docker container on port 5432

Component Diagram
----------------

.. code-block:: text

    Frontend (React)
    ├── Authentication Components
    ├── Dashboard Components
    ├── Calendar View
    ├── Exam Management
    ├── User Management
    ├── Course Management
    ├── Room Management
    └── Group Management
    
    Backend (FastAPI)
    ├── Authentication API
    ├── Exam API
    ├── User API
    ├── Course API
    ├── Room API
    ├── Group API
    └── Email Service
    
    Database (PostgreSQL)
    ├── Users Table
    ├── Professors Table
    ├── Exams Table
    ├── Courses Table
    ├── Rooms Table
    └── Groups Table

Authentication Flow
------------------

The system uses JWT (JSON Web Tokens) for authentication:

1. User submits credentials (email and password)
2. Backend validates credentials and generates a JWT token
3. Token is stored in the browser's local storage
4. Token is included in the Authorization header for subsequent API requests
5. Backend validates the token for each protected endpoint

Data Flow
--------

1. **Exam Creation Process**:
   
   .. code-block:: text

       ┌─────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
       │  Group  │     │ Secretariat │     │  Professor  │     │   System    │
       │  Leader │     │             │     │             │     │             │
       └────┬────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
            │                 │                   │                   │
            │ Propose Exam    │                   │                   │
            ├─────────────────┼───────────────────┼───────────────────►
            │                 │                   │                   │
            │                 │ Create/Edit Exam  │                   │
            │                 ├───────────────────┼───────────────────►
            │                 │                   │                   │
            │                 │                   │ Confirm/Cancel    │
            │                 │                   ├───────────────────►
            │                 │                   │                   │
            │                 │                   │                   │
            │                 │                   │                   │
            │                 │                   │                   │
            ▼                 ▼                   ▼                   ▼

2. **Exam Status Lifecycle**:

   .. code-block:: text

       ┌───────────┐     ┌───────────┐     ┌───────────┐
       │ PROPOSED  │────►│ CONFIRMED │────►│ COMPLETED │
       └─────┬─────┘     └─────┬─────┘     └───────────┘
             │                 │
             │                 │
             ▼                 ▼
       ┌───────────┐     ┌───────────┐
       │ CANCELLED │     │ CANCELLED │
       └───────────┘     └───────────┘

Technology Stack
---------------

**Frontend**:
  * React
  * React Router for navigation
  * Axios for API requests
  * React Big Calendar for calendar view
  * CSS for styling

**Backend**:
  * FastAPI (Python)
  * SQLAlchemy ORM
  * Pydantic for data validation
  * JWT for authentication
  * Docker for containerization

**Database**:
  * PostgreSQL
  * Running in Docker container

**Development & Deployment**:
  * Docker Compose for local development
  * Git for version control
