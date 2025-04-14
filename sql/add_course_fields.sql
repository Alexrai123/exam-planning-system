-- Add new columns to the courses table
ALTER TABLE courses ADD COLUMN IF NOT EXISTS year INTEGER;
ALTER TABLE courses ADD COLUMN IF NOT EXISTS semester INTEGER;
ALTER TABLE courses ADD COLUMN IF NOT EXISTS description TEXT;
