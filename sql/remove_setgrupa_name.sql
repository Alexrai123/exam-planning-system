-- Remove the setGrupa_name field from the grupa table
ALTER TABLE grupa DROP CONSTRAINT IF EXISTS grupa_setgrupa_name_fkey;
ALTER TABLE grupa DROP COLUMN setgrupa_name;
