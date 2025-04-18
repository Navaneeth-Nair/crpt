# GitHub Clone Crypt

GitHub Clone Crypt is a secure, distributed version control system inspired by Git, with a focus on encrypted storage and seamless synchronization between local and remote repositories.

## System Components

The GitHub Clone Crypt system consists of three main components:

1. **CLI Tool (`crpt`)**: A Git-like command-line interface for repository operations
2. **Django Backend**: A server-side API for repository storage and synchronization
3. **React Frontend**: A web interface for browsing and managing repositories

## Features

- Create and manage repositories
- Track file changes with commit history
- Branch and merge support
- Push and pull from remote repositories
- Web interface for repository management
- Secure storage with encryption support

## Installation

### Prerequisites

- Python 3.10+
- MySQL 5.7+ or 8.0+
- Node.js 14+ and npm

### Setting Up the Database

1. Create the MySQL database:

```bash
python create_db.py
```

2. Apply migrations:

```bash
cd crpt_backend
python manage.py migrate
```

### Setting Up the Backend

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Start the Django server:

```bash
cd crpt_backend
python manage.py runserver
```

The backend API will be available at http://127.0.0.1:8000/

### Setting Up the Frontend

1. Install the required npm packages:

```bash
cd frontend/crpt-frontend
npm install
```

2. Start the React development server:

```bash
npm start
```

The frontend will be available at http://localhost:3000/

### Installing the CLI Tool

1. Install the package in development mode:

```bash
pip install -e .
```

2. Verify the installation:

```bash
crpt --version
```

## Usage

### CLI Usage

Create a new repository:
```bash
crpt init
```

Add a file to the staging area:
```bash
crpt add README.md
```

Create a commit:
```bash
crpt commit -m "Initial commit"
```

Push to the remote repository:
```bash
crpt push
```

Pull from the remote repository:
```bash
crpt pull
```

Create a new branch:
```bash
crpt branch develop
```

Switch to a branch:
```bash
crpt checkout develop
```

### Web Interface

1. Visit http://localhost:3000/
2. Create or browse repositories
3. Add files, make commits, and manage branches through the UI

## Architecture

### Database Schema

The system uses a MySQL database with the following tables:

- `remote_repository`: Stores repository information
- `remote_commit`: Stores commit details and history
- `remote_blob`: Stores file contents (blobs)

For more details, see [database_schema.md](database_schema.md).

### System Flow

1. Local repositories are managed via the CLI (`crpt`)
2. The CLI communicates with the Django backend API for push/pull operations
3. The React frontend provides a web interface to interact with the backend

## Development

### Directory Structure

- `crpt/`: CLI tool and core functionality
- `crpt_backend/`: Django backend configuration
- `remote/`: Django app for repository management
- `frontend/crpt-frontend/`: React frontend application

### Adding Features

To add new features:

1. Update the models in `remote/models.py` if needed
2. Create migrations with `python manage.py makemigrations`
3. Apply migrations with `python manage.py migrate`
4. Update the API endpoints in `remote/views.py`
5. Update the CLI commands in `crpt/crpt.py`
6. Update the frontend components as needed

## License

[MIT License](LICENSE)

## Contributors

- Your Name