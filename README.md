# Git-Backed Messaging Application

A web-based messaging application that uses Git as a backend storage system. Messages are stored in a SQLite database and synchronized with GitHub, providing version control and backup for all conversations.

## Features

- Real-time messaging interface
- SQLite database for local message storage
- Git integration for message backup and version control
- GitHub API integration for remote synchronization
- Simple and lightweight design (no frameworks)
- Secure authentication using GitHub tokens

## Tech Stack

- Backend: Python (with built-in libraries)
- Database: SQLite3
- Frontend: HTML5, CSS3, JavaScript (vanilla)
- Version Control: Git
- APIs: GitHub REST API

## Project Structure

```
testchat/
├── README.md
├── .env                  # Environment variables (GitHub token)
├── .gitignore           # Git ignore file
├── app.py               # Main Python application
├── database/
│   ├── schema.sql       # Database schema
│   └── db.sqlite        # SQLite database file
├── static/
│   ├── css/
│   │   └── style.css    # Application styles
│   └── js/
│       └── main.js      # Frontend JavaScript
└── templates/
    └── index.html       # Main HTML template
```

## Prerequisites

- Python 3.8 or higher
- Git installed and configured
- GitHub account with personal access token
- SQLite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/wpinney/testchat.git
cd testchat
```

2. Create and configure your `.env` file:
```bash
GITHUB_TOKEN=your_github_token
```

3. Initialize the database:
```bash
python init_db.py
```

4. Start the application:
```bash
python app.py
```

## Development Roadmap

1. Basic Setup
   - Project structure
   - Environment configuration
   - Git integration

2. Database Layer
   - SQLite schema design
   - Database initialization
   - CRUD operations

3. Backend Development
   - Python server setup
   - GitHub API integration
   - Message synchronization

4. Frontend Development
   - HTML structure
   - CSS styling
   - JavaScript functionality

5. Integration
   - Connect frontend with backend
   - Implement real-time updates
   - Add Git synchronization

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License.

## Last Updated

2025-01-07
