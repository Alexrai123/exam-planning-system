-- Add leader_id to the grupa table
ALTER TABLE grupa ADD COLUMN leader_id INTEGER REFERENCES users(id);

-- Create an index for faster lookups
CREATE INDEX ix_grupa_leader_id ON grupa(leader_id);
