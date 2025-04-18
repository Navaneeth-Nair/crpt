-- GitHub Clone Crypt - MySQL Schema Definition
-- This file contains the complete SQL schema for the application

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS github_clone_crypt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE github_clone_crypt;

-- Repository table
CREATE TABLE IF NOT EXISTS remote_repository (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Commit table
CREATE TABLE IF NOT EXISTS remote_commit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    repo_id INT NOT NULL,
    commit_id VARCHAR(40) NOT NULL UNIQUE,
    message TEXT NOT NULL,
    branch VARCHAR(100) NOT NULL,
    parent VARCHAR(40) NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (repo_id) REFERENCES remote_repository(id) ON DELETE CASCADE
);

-- Create index for faster lookups
CREATE INDEX idx_commit_repo ON remote_commit(repo_id);
CREATE INDEX idx_commit_hash ON remote_commit(commit_id);

-- Blob table (file contents)
CREATE TABLE IF NOT EXISTS remote_blob (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commit_id INT NOT NULL,
    path VARCHAR(255) NOT NULL,
    hash VARCHAR(40) NOT NULL,
    content LONGBLOB NOT NULL,
    FOREIGN KEY (commit_id) REFERENCES remote_commit(id) ON DELETE CASCADE
);

-- Create index for faster lookups
CREATE INDEX idx_blob_commit ON remote_blob(commit_id);

-- Add sample data (optional, for testing)
-- INSERT INTO remote_repository (name) VALUES ('sample-repo');
-- INSERT INTO remote_commit (repo_id, commit_id, message, branch) VALUES (1, 'abcdef1234567890', 'Initial commit', 'main');
-- INSERT INTO remote_blob (commit_id, path, hash, content) VALUES (1, 'README.md', 'abc123', 'IyBSZWFkbWUK');