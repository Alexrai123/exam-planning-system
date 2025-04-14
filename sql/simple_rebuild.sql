-- Create a backup of the current data
CREATE TEMPORARY TABLE temp_users AS SELECT * FROM users;
CREATE TEMPORARY TABLE temp_professors AS SELECT * FROM professors;
CREATE TEMPORARY TABLE temp_grupa AS SELECT * FROM grupa;
CREATE TEMPORARY TABLE temp_courses AS SELECT * FROM courses;
CREATE TEMPORARY TABLE temp_sala AS SELECT * FROM sala;
CREATE TEMPORARY TABLE temp_exams AS SELECT * FROM exams;

-- Drop constraints to allow table modifications
ALTER TABLE exams DROP CONSTRAINT exams_grupa_id_fkey;
ALTER TABLE exams DROP CONSTRAINT exams_course_id_fkey;
ALTER TABLE exams DROP CONSTRAINT exams_sala_id_fkey;

-- Modify the grupa table to use name as primary key
ALTER TABLE grupa DROP CONSTRAINT grupa_pkey;
ALTER TABLE grupa ADD COLUMN name_temp VARCHAR(50);
UPDATE grupa SET name_temp = name;
ALTER TABLE grupa DROP COLUMN id;
ALTER TABLE grupa RENAME COLUMN name_temp TO name;
ALTER TABLE grupa ADD PRIMARY KEY (name);

-- Add the new columns to grupa
ALTER TABLE grupa ADD COLUMN setGrupa_name VARCHAR(50);
UPDATE grupa g SET setGrupa_name = (
    SELECT sg.name FROM temp_grupa sg WHERE sg.id = g.setGrupa_id
);
ALTER TABLE grupa DROP COLUMN setGrupa_id;

-- Modify the exams table to reference grupa by name
ALTER TABLE exams ADD COLUMN grupa_name VARCHAR(50);
UPDATE exams e SET grupa_name = (
    SELECT g.name FROM temp_grupa g WHERE g.id = e.grupa_id
);
ALTER TABLE exams DROP COLUMN grupa_id;

-- Recreate the foreign key constraints
ALTER TABLE exams ADD CONSTRAINT exams_grupa_name_fkey 
    FOREIGN KEY (grupa_name) REFERENCES grupa(name);
ALTER TABLE exams ADD CONSTRAINT exams_course_id_fkey 
    FOREIGN KEY (course_id) REFERENCES courses(id);
ALTER TABLE exams ADD CONSTRAINT exams_sala_id_fkey 
    FOREIGN KEY (sala_id) REFERENCES sala(id);

-- Add foreign key constraint for setGrupa_name
ALTER TABLE grupa ADD CONSTRAINT grupa_setgrupa_name_fkey 
    FOREIGN KEY (setGrupa_name) REFERENCES grupa(name);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS ix_grupa_name ON grupa(name);
CREATE INDEX IF NOT EXISTS ix_exams_grupa_name ON exams(grupa_name);
