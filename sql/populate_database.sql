-- Populate the database with sample data

-- Users (STUDENT, PROFESSOR, SECRETARIAT)
INSERT INTO users (name, email, password, role) VALUES
('Admin User', 'admin@example.com', '$2b$12$1234567890123456789012uQSAFVCX/5yvzMHXjYmZnDQcY3Z7xTO', 'SECRETARIAT'),
('John Smith', 'john.smith@example.com', '$2b$12$1234567890123456789012uQSAFVCX/5yvzMHXjYmZnDQcY3Z7xTO', 'PROFESSOR'),
('Maria Johnson', 'maria.johnson@example.com', '$2b$12$1234567890123456789012uQSAFVCX/5yvzMHXjYmZnDQcY3Z7xTO', 'PROFESSOR'),
('Robert Davis', 'robert.davis@example.com', '$2b$12$1234567890123456789012uQSAFVCX/5yvzMHXjYmZnDQcY3Z7xTO', 'PROFESSOR'),
('Emma Wilson', 'emma.wilson@example.com', '$2b$12$1234567890123456789012uQSAFVCX/5yvzMHXjYmZnDQcY3Z7xTO', 'STUDENT'),
('Michael Brown', 'michael.brown@example.com', '$2b$12$1234567890123456789012uQSAFVCX/5yvzMHXjYmZnDQcY3Z7xTO', 'STUDENT'),
('Sophia Garcia', 'sophia.garcia@example.com', '$2b$12$1234567890123456789012uQSAFVCX/5yvzMHXjYmZnDQcY3Z7xTO', 'STUDENT'),
('David Martinez', 'david.martinez@example.com', '$2b$12$1234567890123456789012uQSAFVCX/5yvzMHXjYmZnDQcY3Z7xTO', 'STUDENT');

-- Professors (linked to users with PROFESSOR role)
INSERT INTO professors (name, specialization, title, user_id) VALUES
('John Smith', 'Computer Science', 'Professor', 2),
('Maria Johnson', 'Mathematics', 'Associate Professor', 3),
('Robert Davis', 'Physics', 'Assistant Professor', 4);

-- Rooms
INSERT INTO sala (name) VALUES
('A101'),
('B202'),
('C303'),
('D404'),
('E505');

-- Groups
INSERT INTO grupa (name, year, specialization, leader_id) VALUES
('CS101', 1, 'Computer Science', 5),
('CS201', 2, 'Computer Science', 6),
('MATH101', 1, 'Mathematics', 7),
('PHYS101', 1, 'Physics', 8);

-- Courses
INSERT INTO courses (name, profesor_name, credits) VALUES
('Introduction to Programming', 'John Smith', 6),
('Data Structures and Algorithms', 'John Smith', 5),
('Calculus I', 'Maria Johnson', 6),
('Mechanics', 'Robert Davis', 5);

-- Exams (some in the future, some in the past)
INSERT INTO exams (course_id, grupa_name, date, time, sala_name, status) VALUES
(1, 'CS101', '2025-06-15', '09:00:00', 'A101', 'PROPOSED'),
(2, 'CS201', '2025-06-18', '14:00:00', 'B202', 'PROPOSED'),
(3, 'MATH101', '2025-06-20', '10:00:00', 'C303', 'CONFIRMED'),
(4, 'PHYS101', '2025-06-22', '12:00:00', 'D404', 'CONFIRMED');
