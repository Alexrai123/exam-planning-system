-- First, we need to check if there are any exams referencing grupa
-- If there are, we need to temporarily disable the foreign key constraint
ALTER TABLE exams DROP CONSTRAINT exams_grupa_id_fkey;

-- Also drop the self-reference constraint
ALTER TABLE grupa DROP CONSTRAINT grupa_setgrupa_id_fkey;

-- Create a temporary table to store the mapping between old IDs and names
CREATE TEMPORARY TABLE grupa_id_mapping (
    old_id INTEGER,
    name VARCHAR(50)
);

-- Populate the temporary table
INSERT INTO grupa_id_mapping
SELECT id, name FROM grupa;

-- Create a new grupa table with name as the primary key
CREATE TABLE new_grupa (
    name VARCHAR(50) PRIMARY KEY,
    setGrupa_name VARCHAR(50) REFERENCES new_grupa(name),
    year INTEGER,
    specialization VARCHAR(100)
);

-- Copy data to the new table
INSERT INTO new_grupa (name, setGrupa_name, year, specialization)
SELECT 
    g.name, 
    (SELECT m.name FROM grupa_id_mapping m WHERE m.old_id = g.setGrupa_id),
    g.year,
    g.specialization
FROM grupa g;

-- Update exams to reference the new grupa names
ALTER TABLE exams RENAME COLUMN grupa_id TO grupa_id_old;
ALTER TABLE exams ADD COLUMN grupa_name VARCHAR(50);

UPDATE exams e
SET grupa_name = (
    SELECT m.name FROM grupa_id_mapping m WHERE m.old_id = e.grupa_id_old
);

-- Drop the old grupa table
DROP TABLE grupa;

-- Rename the new table to grupa
ALTER TABLE new_grupa RENAME TO grupa;

-- Create an index on the name column
CREATE INDEX ix_grupa_name ON grupa(name);

-- Modify the exams table to use grupa name as foreign key
ALTER TABLE exams 
    DROP COLUMN grupa_id_old,
    ALTER COLUMN grupa_name SET NOT NULL,
    ADD CONSTRAINT exams_grupa_name_fkey FOREIGN KEY (grupa_name) REFERENCES grupa(name);

-- Update the sequence for grupa_id_seq (if needed for other tables)
-- This is optional and depends on your application
-- DROP SEQUENCE IF EXISTS grupa_id_seq;
