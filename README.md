# Basic Chat Application

A simple real-time chat application that allows users to communicate with each other.

## Features

- Real-time messaging
- Simple and intuitive user interface
- Support for multiple users
- Text-based communication

## Prerequisites

- Python 3.8 or higher
- Flask
- Flask-SocketIO
- HTML/CSS/JavaScript knowledge (for frontend development)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd testchat
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## GitHub Token Setup

1. Copy the `.env.template` file to create a new `.env` file:
```bash
cp .env.template .env
```

2. Edit the `.env` file and replace `your_github_token_here` with your actual GitHub token.

3. To create a new GitHub token:
   - Go to GitHub Settings > Developer Settings > Personal Access Tokens
   - Generate a new token with the necessary repository permissions
   - Copy the token and paste it in your `.env` file

Note: Never commit your `.env` file or share your GitHub token.

## Usage

1. Start the server:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Start chatting!

## Project Structure

```
testchat/
├── README.md
├── app.py
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/
    └── index.html
```

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Last Updated

2025-01-07
