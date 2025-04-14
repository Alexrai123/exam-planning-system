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
