-- Add user_id to professors table to link back to users
ALTER TABLE professors ADD COLUMN user_id INTEGER REFERENCES users(id);
CREATE INDEX ix_professors_user_id ON professors(user_id);

-- Add user_id to grupa table for the leader
ALTER TABLE grupa DROP COLUMN IF EXISTS leader_name;
ALTER TABLE grupa ADD COLUMN leader_id INTEGER REFERENCES users(id);
CREATE INDEX ix_grupa_leader_id ON grupa(leader_id);
