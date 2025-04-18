# GitHub Clone Crypt - Database Schema

## Database Overview

The GitHub Clone Crypt system uses a MySQL database to store repository information, commits, and file content (blobs). This document outlines the database schema used by the application.

## Database: `github_clone_crypt`

### Table: `remote_repository`

Stores basic information about repositories in the system.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the repository |
| name | VARCHAR(100) | NOT NULL | Name of the repository |

### Table: `remote_commit`

Stores commit information including messages, branches, and parent relationships.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the commit |
| repo_id | INT | FOREIGN KEY (remote_repository.id) | Reference to the repository |
| commit_id | VARCHAR(40) | UNIQUE, NOT NULL | The SHA-1 hash of the commit |
| message | TEXT | NOT NULL | Commit message |
| branch | VARCHAR(100) | NOT NULL | Branch where the commit belongs |
| parent | VARCHAR(40) | NULL | SHA-1 hash of parent commit (null for initial commits) |
| timestamp | DATETIME | NOT NULL | When the commit was created |

### Table: `remote_blob`

Stores file contents for each commit.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the blob |
| commit_id | INT | FOREIGN KEY (remote_commit.id) | Reference to the commit |
| path | VARCHAR(255) | NOT NULL | File path within the repository |
| hash | VARCHAR(40) | NOT NULL | SHA-1 hash of the file content |
| content | LONGBLOB | NOT NULL | Binary content of the file |

## Relationships

1. **Repository to Commits**: One-to-Many
   - A repository can have multiple commits
   - Each commit belongs to exactly one repository

2. **Commit to Blobs**: One-to-Many
   - A commit can contain multiple blob changes (files)
   - Each blob belongs to exactly one commit

3. **Commit to Commit** (Self-reference): Parent-Child
   - A commit can have one parent commit (referenced by parent field)
   - A commit can have multiple child commits

## Indexes

- `remote_commit.commit_id`: Indexed for fast lookups by commit hash
- `remote_commit.repo_id`: Indexed for fast filtering commits by repository
- `remote_blob.commit_id`: Indexed for fast retrieval of blobs related to a commit

## Data Flow

1. When a user creates a repository, a new entry is added to `remote_repository`
2. When a commit is made:
   - A new entry is added to `remote_commit` with reference to its repository
   - For each changed file, a blob is created in `remote_blob` with reference to the commit
3. When retrieving repository data:
   - First fetch the repository details from `remote_repository`
   - Then get the relevant commits from `remote_commit`
   - Finally, get the associated blobs from `remote_blob`

This schema efficiently supports Git-like operations including branching, commit history, and file management while providing a robust foundation for the GitHub Clone Crypt system.