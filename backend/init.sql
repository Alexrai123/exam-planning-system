-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert admin user (password is hashed version of 'password')
INSERT INTO users (email, password, full_name, role, is_active)
VALUES 
('admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Admin User', 'secretariat', true)
ON CONFLICT (email) DO NOTHING;

-- Insert professor user
INSERT INTO users (email, password, full_name, role, is_active)
VALUES 
('professor@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Professor User', 'professor', true)
ON CONFLICT (email) DO NOTHING;

-- Insert student user
INSERT INTO users (email, password, full_name, role, is_active)
VALUES 
('student@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Student User', 'student', true)
ON CONFLICT (email) DO NOTHING;
