# PowerShell script to recreate the database with the new schema

# Create a backup of the current database first
Write-Host "Creating a backup of the current database..."
docker exec exam_planning_db pg_dump -U postgres -d exam_planning > ./exam_planning_backup_full.sql

# Create a script to drop and recreate the database
$recreateScript = @"
-- Drop and recreate the database
DROP DATABASE exam_planning;
CREATE DATABASE exam_planning;
"@

# Write the recreate script to a file
$recreateScript | Out-File -FilePath "./recreate_database.sql" -Encoding utf8

# Copy the recreate script to the Docker container
Write-Host "Copying recreate script to the Docker container..."
docker cp ./recreate_database.sql exam_planning_db:/tmp/recreate_database.sql

# Execute the recreate script
Write-Host "Recreating the database..."
docker exec exam_planning_db psql -U postgres -f /tmp/recreate_database.sql

# Now create a script with the new schema
$schemaScript = @"
-- Connect to the new database
\c exam_planning

-- Create enum types
CREATE TYPE userrole AS ENUM ('STUDENT', 'PROFESSOR', 'SECRETARIAT');
CREATE TYPE examstatus AS ENUM ('PROPOSED', 'CONFIRMED', 'CANCELLED', 'COMPLETED');

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    role userrole NOT NULL
);
CREATE INDEX ix_users_id ON users(id);
CREATE INDEX ix_users_email ON users(email);

-- Create professors table
CREATE TABLE professors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    department VARCHAR(100),
    title VARCHAR(50)
);
CREATE INDEX idx_professors_user_id ON professors(user_id);

-- Create grupa table with name as primary key
CREATE TABLE grupa (
    name VARCHAR(50) PRIMARY KEY,
    setGrupa_name VARCHAR(50) REFERENCES grupa(name),
    year INTEGER,
    specialization VARCHAR(100)
);
CREATE INDEX ix_grupa_name ON grupa(name);

-- Create courses table
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    profesor_id INTEGER NOT NULL REFERENCES users(id),
    credits INTEGER
);
CREATE INDEX ix_courses_id ON courses(id);

-- Create sala table
CREATE TABLE sala (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);
CREATE INDEX ix_sala_id ON sala(id);

-- Create exams table
CREATE TABLE exams (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id),
    grupa_name VARCHAR(50) NOT NULL REFERENCES grupa(name),
    date DATE NOT NULL,
    time TIME NOT NULL,
    sala_id INTEGER NOT NULL REFERENCES sala(id),
    status examstatus NOT NULL DEFAULT 'PROPOSED'
);
CREATE INDEX ix_exams_id ON exams(id);
"@

# Write the schema script to a file
$schemaScript | Out-File -FilePath "./new_schema.sql" -Encoding utf8

# Copy the schema script to the Docker container
Write-Host "Copying schema script to the Docker container..."
docker cp ./new_schema.sql exam_planning_db:/tmp/new_schema.sql

# Execute the schema script
Write-Host "Creating new schema..."
docker exec exam_planning_db psql -U postgres -f /tmp/new_schema.sql

# Restart the backend to apply changes
Write-Host "Restarting the backend..."
docker restart exam_planning_backend

Write-Host "Database recreation complete! You'll need to reinitialize your data."
