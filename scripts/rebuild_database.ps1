# PowerShell script to rebuild the database with the updated schema

# Create a backup of the current database
Write-Host "Creating a backup of the current database..."
docker exec exam_planning_db pg_dump -U postgres -d exam_planning > ./exam_planning_backup_full.sql

# Create a new SQL script to rebuild the database
Write-Host "Creating a new database schema..."
$rebuildScript = @"
-- Drop the database and recreate it
DROP DATABASE IF EXISTS exam_planning;
CREATE DATABASE exam_planning;

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
    name VARCHAR(50) NOT NULL
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

# Write the rebuild script to a file
$rebuildScript | Out-File -FilePath "./rebuild_database.sql" -Encoding utf8

# Copy the rebuild script to the Docker container
Write-Host "Copying rebuild script to the Docker container..."
docker cp ./rebuild_database.sql exam_planning_db:/tmp/rebuild_database.sql

# Execute the rebuild script
Write-Host "Rebuilding the database..."
docker exec exam_planning_db psql -U postgres -f /tmp/rebuild_database.sql

# Now create a script to import the data with transformations
Write-Host "Creating data import script..."
$importScript = @"
-- Import users data
INSERT INTO users (id, name, email, password, role)
SELECT id, name, email, password, role
FROM temp_users;

-- Import professors data
INSERT INTO professors (id, user_id, department, title)
SELECT id, user_id, department, title
FROM temp_professors;

-- Import grupa data with name as primary key
INSERT INTO grupa (name, setGrupa_name, year, specialization)
SELECT g.name, 
       (SELECT sg.name FROM temp_grupa sg WHERE sg.id = g.setGrupa_id),
       g.year, 
       g.specialization
FROM temp_grupa g;

-- Import courses data
INSERT INTO courses (id, name, profesor_id, credits)
SELECT id, name, profesor_id, credits
FROM temp_courses;

-- Import sala data
INSERT INTO sala (id, name)
SELECT id, name
FROM temp_sala;

-- Import exams data with grupa_name instead of grupa_id
INSERT INTO exams (id, course_id, grupa_name, date, time, sala_id, status)
SELECT e.id, 
       e.course_id, 
       (SELECT g.name FROM temp_grupa g WHERE g.id = e.grupa_id),
       e.date, 
       e.time, 
       e.sala_id, 
       e.status
FROM temp_exams e;
"@

$importScript | Out-File -FilePath "./import_data.sql" -Encoding utf8

# Create a script to extract data from the backup
Write-Host "Creating data extraction script..."
$extractScript = @"
-- Create temporary tables to hold the data
CREATE TEMPORARY TABLE temp_users AS
SELECT * FROM users;

CREATE TEMPORARY TABLE temp_professors AS
SELECT * FROM professors;

CREATE TEMPORARY TABLE temp_grupa AS
SELECT * FROM grupa;

CREATE TEMPORARY TABLE temp_courses AS
SELECT * FROM courses;

CREATE TEMPORARY TABLE temp_sala AS
SELECT * FROM sala;

CREATE TEMPORARY TABLE temp_exams AS
SELECT * FROM exams;
"@

$extractScript | Out-File -FilePath "./extract_data.sql" -Encoding utf8

# Copy the extraction and import scripts to the Docker container
Write-Host "Copying data scripts to the Docker container..."
docker cp ./extract_data.sql exam_planning_db:/tmp/extract_data.sql
docker cp ./import_data.sql exam_planning_db:/tmp/import_data.sql

# Execute the extraction script on the backup
Write-Host "Extracting data from backup..."
docker exec exam_planning_db psql -U postgres -d exam_planning -f /tmp/extract_data.sql

# Execute the import script
Write-Host "Importing data with transformations..."
docker exec exam_planning_db psql -U postgres -d exam_planning -f /tmp/import_data.sql

# Restart the backend to apply changes
Write-Host "Restarting the backend..."
docker restart exam_planning_backend

Write-Host "Database rebuild complete!"
