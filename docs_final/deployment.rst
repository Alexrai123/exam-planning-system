Deployment
==========

This section explains how to deploy the Exam Planning System.

Prerequisites
------------

- Docker and Docker Compose
- Git
- Node.js and npm (for frontend development)
- Python 3.8+ (for local development)

Docker Deployment
---------------

The Exam Planning System is designed to run in Docker containers, which simplifies deployment and ensures consistency across environments.

1. **Clone the Repository**:

   .. code-block:: bash

      git clone <repository-url>
      cd proiect-gherman

2. **Start the Docker Containers**:

   .. code-block:: bash

      docker-compose up -d

   This will start the following containers:
   
   - PostgreSQL database (`exam_planning_db`) on port 5432
   - FastAPI backend (`exam_planning_backend`) on port 8000

3. **Start the Frontend Development Server**:

   .. code-block:: bash

      cd frontend
      npm install
      npm start

   This will start the React development server on port 3000.

4. **Access the Application**:

   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

Database Initialization
---------------------

The database is automatically initialized when the containers start. If you need to reset the database or apply migrations, you can use the provided scripts:

1. **Reset the Database**:

   .. code-block:: bash

      powershell -ExecutionPolicy Bypass -File .\recreate_database.ps1

2. **Apply Migrations**:

   .. code-block:: bash

      powershell -ExecutionPolicy Bypass -File .\apply_migrations.ps1

3. **Populate with Sample Data**:

   .. code-block:: bash

      powershell -ExecutionPolicy Bypass -File .\run_populate_database.ps1

Environment Variables
------------------

The application uses environment variables for configuration. These are defined in the `docker-compose.yml` file:

.. code-block:: yaml

   environment:
     - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/exam_planning
     - SECRET_KEY=your_secret_key_here
     - JWT_SECRET_KEY=your_jwt_secret_key_here
     - MAIL_SERVER=smtp.example.com
     - MAIL_PORT=587
     - MAIL_USERNAME=your_email@example.com
     - MAIL_PASSWORD=your_email_password
     - MAIL_USE_TLS=True

Production Deployment
-------------------

For production deployment, additional steps are recommended:

1. **Use a Production-Ready Database**:
   
   Consider using a managed PostgreSQL service like AWS RDS or Azure Database for PostgreSQL.

2. **Set Up HTTPS**:
   
   Use a reverse proxy like Nginx with Let's Encrypt for SSL/TLS.

3. **Build the Frontend for Production**:

   .. code-block:: bash

      cd frontend
      npm run build

   Then serve the static files from a web server or CDN.

4. **Set Secure Environment Variables**:
   
   Use a secure method to manage environment variables in production, such as Docker secrets or a dedicated secrets management service.

5. **Set Up Monitoring and Logging**:
   
   Implement monitoring and logging solutions to track application performance and errors.

Troubleshooting
-------------

1. **Database Connection Issues**:
   
   - Verify that the PostgreSQL container is running: `docker ps`
   - Check the database logs: `docker logs exam_planning_db`
   - Ensure the DATABASE_URL environment variable is correct

2. **Backend API Issues**:
   
   - Check the backend logs: `docker logs exam_planning_backend`
   - Verify that the backend container is running: `docker ps`
   - Try accessing the API documentation: http://localhost:8000/docs

3. **Frontend Issues**:
   
   - Check the frontend development server logs
   - Verify that the backend API is accessible from the frontend
   - Check for CORS issues in the browser console
