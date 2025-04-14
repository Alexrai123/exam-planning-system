-- Add new fields to the sala table
ALTER TABLE sala ADD COLUMN IF NOT EXISTS building VARCHAR(50);
ALTER TABLE sala ADD COLUMN IF NOT EXISTS capacity INTEGER;
ALTER TABLE sala ADD COLUMN IF NOT EXISTS computers INTEGER;

-- Add new fields to the professors table
ALTER TABLE professors ADD COLUMN IF NOT EXISTS email VARCHAR(100);
ALTER TABLE professors ADD COLUMN IF NOT EXISTS phone VARCHAR(20);
ALTER TABLE professors ADD COLUMN IF NOT EXISTS faculty VARCHAR(100);

-- Create an index on the name columns for better performance
CREATE INDEX IF NOT EXISTS idx_sala_name ON sala(name);
CREATE INDEX IF NOT EXISTS idx_professors_name ON professors(name);
CREATE INDEX IF NOT EXISTS idx_grupa_name ON grupa(name);
