-- Create and use ai_hire database
CREATE DATABASE IF NOT EXISTS ai_hire;
USE ai_hire;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role ENUM('candidate','hr','admin') DEFAULT 'candidate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resumes table
CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    resume_name VARCHAR(255),
    resume_path VARCHAR(500),
    ats_score INT DEFAULT 0,
    uploaded_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Jobs table
CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(255),
    company_name VARCHAR(255),
    experience VARCHAR(50),
    location VARCHAR(255),
    skills TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Applications table
CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    job_id INT,
    job_title VARCHAR(255),
    company VARCHAR(255),
    location VARCHAR(255),
    ats_score INT,
    jd_match INT,
    applied_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('applied','reviewed','accepted','rejected') DEFAULT 'applied',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);
