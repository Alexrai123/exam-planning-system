-- First, drop the existing leader_id column
ALTER TABLE grupa DROP COLUMN IF EXISTS leader_id;

-- Add a new leader_name column that's unique
ALTER TABLE grupa ADD COLUMN leader_name VARCHAR(100) UNIQUE;

-- Create an index for faster lookups
CREATE INDEX ix_grupa_leader_name ON grupa(leader_name);
