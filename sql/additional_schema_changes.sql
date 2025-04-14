-- Make changes to sala table: make name the primary key and remove id
-- First, drop constraints that reference sala.id
ALTER TABLE exams DROP CONSTRAINT exams_sala_id_fkey;

-- Add a temporary column to store the sala name
ALTER TABLE exams ADD COLUMN sala_name VARCHAR(50);

-- Update the sala_name column with the corresponding sala names
UPDATE exams e SET sala_name = (SELECT s.name FROM sala s WHERE s.id = e.sala_id);

-- Drop the sala_id column
ALTER TABLE exams DROP COLUMN sala_id;

-- Modify the sala table
ALTER TABLE sala DROP CONSTRAINT sala_pkey;
ALTER TABLE sala DROP CONSTRAINT sala_name_key;
ALTER TABLE sala ADD PRIMARY KEY (name);
ALTER TABLE sala DROP COLUMN id;

-- Add foreign key constraint from exams to sala
ALTER TABLE exams ADD CONSTRAINT exams_sala_name_fkey FOREIGN KEY (sala_name) REFERENCES sala(name);

-- Make changes to professors table
-- First, drop constraints that reference professors
ALTER TABLE professors DROP CONSTRAINT professors_user_id_fkey;

-- Modify the courses table to reference professor name instead of user id
ALTER TABLE courses RENAME COLUMN profesor_id TO profesor_id_old;
ALTER TABLE courses ADD COLUMN profesor_name VARCHAR(100);

-- Create a new professors table with name as primary key
CREATE TABLE new_professors (
    name VARCHAR(100) PRIMARY KEY,
    specialization VARCHAR(100),
    title VARCHAR(50)
);

-- Insert data from the old professors table into the new one
-- We'll use the user's name as the professor's name
INSERT INTO new_professors (name, specialization, title)
SELECT u.name, p.department, p.title
FROM professors p
JOIN users u ON p.user_id = u.id;

-- Update the courses table to reference professor names
UPDATE courses c SET profesor_name = (
    SELECT u.name 
    FROM users u 
    WHERE u.id = c.profesor_id_old
);

-- Drop the old professors table
DROP TABLE professors;

-- Rename the new professors table
ALTER TABLE new_professors RENAME TO professors;

-- Add foreign key constraint from courses to professors
ALTER TABLE courses DROP COLUMN profesor_id_old;
ALTER TABLE courses ALTER COLUMN profesor_name SET NOT NULL;
ALTER TABLE courses ADD CONSTRAINT courses_profesor_name_fkey FOREIGN KEY (profesor_name) REFERENCES professors(name);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS ix_sala_name ON sala(name);
CREATE INDEX IF NOT EXISTS ix_professors_name ON professors(name);
CREATE INDEX IF NOT EXISTS ix_exams_sala_name ON exams(sala_name);
