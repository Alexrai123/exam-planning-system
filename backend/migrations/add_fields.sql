-- Add fields to grupa table
ALTER TABLE grupa 
ADD COLUMN IF NOT EXISTS year INTEGER,
ADD COLUMN IF NOT EXISTS specialization VARCHAR(100);

-- Add credits field to courses table
ALTER TABLE courses
ADD COLUMN IF NOT EXISTS credits INTEGER;

-- Create a new table for professors (optional approach)
-- This allows storing professor details separately while maintaining the relationship
CREATE TABLE IF NOT EXISTS professors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
    department VARCHAR(100),
    title VARCHAR(50),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Optional: Add an index on the user_id column for faster lookups
CREATE INDEX IF NOT EXISTS idx_professors_user_id ON professors(user_id);

-- Comment out the following if you decide not to use the professors table
-- ALTER TABLE courses
-- DROP CONSTRAINT courses_profesor_id_fkey,
-- ADD CONSTRAINT courses_profesor_id_fkey FOREIGN KEY (profesor_id) REFERENCES professors(id);
