-- Insert admin user (password is hashed version of 'password')
INSERT INTO users (name, email, password, role)
VALUES 
('Admin User', 'admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'SECRETARIAT')
ON CONFLICT (email) DO NOTHING;

-- Insert professor user
INSERT INTO users (name, email, password, role)
VALUES 
('Professor User', 'professor@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'PROFESSOR')
ON CONFLICT (email) DO NOTHING;

-- Insert student user
INSERT INTO users (name, email, password, role)
VALUES 
('Student User', 'student@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'STUDENT')
ON CONFLICT (email) DO NOTHING;
