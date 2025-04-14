-- Update user roles to ensure correct capitalization
UPDATE users SET role = 'SECRETARIAT' WHERE role = 'secretariat';
UPDATE users SET role = 'PROFESSOR' WHERE role = 'professor';
UPDATE users SET role = 'STUDENT' WHERE role = 'student';
