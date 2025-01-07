#!/usr/bin/env python3
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GitManager:
    def __init__(self, repo_url: str):
        self.repo_url = repo_url
        self.github_token = os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            raise ValueError("GitHub token not found in environment variables")
        
        # Setup repository paths
        self.base_path = Path(__file__).parent
        self.messages_dir = self.base_path / 'messages'
        self.messages_dir.mkdir(exist_ok=True)

    def clone_repository(self) -> bool:
        """Clone the repository if it doesn't exist"""
        try:
            # Check if repository already exists
            if (self.base_path / '.git').exists():
                print("Repository already exists locally")
                return True

            # Construct clone URL with token
            clone_url = f"https://{self.github_token}@github.com/{self.repo_url.split('github.com/')[1]}"
            
            # Clone the repository
            result = subprocess.run(
                ['git', 'clone', clone_url, '.'],
                cwd=str(self.base_path),
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Error cloning repository: {result.stderr}")
                return False
                
            return True
            
        except Exception as e:
            print(f"Error in clone_repository: {e}")
            return False

    def create_message_file(self, content: str, sender: str) -> Optional[str]:
        """Create a new file containing the message"""
        try:
            # Create timestamp and filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"message_{timestamp}.json"
            filepath = self.messages_dir / filename

            # Create message data
            message_data = {
                'content': content,
                'sender': sender,
                'timestamp': datetime.now().isoformat()
            }

            # Write message to file
            with open(filepath, 'w') as f:
                json.dump(message_data, f, indent=2)

            return str(filepath)

        except Exception as e:
            print(f"Error creating message file: {e}")
            return None

    def push_message(self, filepath: str) -> Optional[str]:
        """Push a message file to GitHub and return the commit hash"""
        try:
            # Add the file
            add_result = subprocess.run(
                ['git', 'add', filepath],
                cwd=str(self.base_path),
                capture_output=True,
                text=True
            )
            if add_result.returncode != 0:
                raise Exception(f"Git add failed: {add_result.stderr}")

            # Create commit
            commit_result = subprocess.run(
                ['git', 'commit', '-m', f"Add message: {Path(filepath).name}"],
                cwd=str(self.base_path),
                capture_output=True,
                text=True
            )
            if commit_result.returncode != 0:
                raise Exception(f"Git commit failed: {commit_result.stderr}")

            # Push changes
            push_result = subprocess.run(
                ['git', 'push', 'origin', 'master'],
                cwd=str(self.base_path),
                capture_output=True,
                text=True
            )
            if push_result.returncode != 0:
                raise Exception(f"Git push failed: {push_result.stderr}")

            # Get commit hash
            hash_result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=str(self.base_path),
                capture_output=True,
                text=True
            )
            if hash_result.returncode != 0:
                raise Exception(f"Failed to get commit hash: {hash_result.stderr}")

            return hash_result.stdout.strip()

        except Exception as e:
            print(f"Error in push_message: {e}")
            return None

    def get_message_history(self) -> List[Dict]:
        """Get the history of messages from the repository"""
        messages = []
        try:
            # Ensure the messages directory exists
            self.messages_dir.mkdir(exist_ok=True)
            
            # Get all message files
            message_files = sorted(self.messages_dir.glob('message_*.json'))
            
            for file in message_files:
                try:
                    with open(file, 'r') as f:
                        message_data = json.load(f)
                        messages.append(message_data)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error reading message file {file}: {e}")
                    continue
                    
            # Sort messages by timestamp
            return sorted(messages, key=lambda x: x['timestamp'])
            
        except Exception as e:
            print(f"Error getting message history: {e}")
            return []

def main():
    """Test the GitManager functionality"""
    # Get repository URL from command line or use default
    repo_url = "https://github.com/wpinney/testchat.git"
    
    try:
        # Initialize GitManager
        git_manager = GitManager(repo_url)
        
        # Ensure repository is cloned
        if not git_manager.clone_repository():
            print("Failed to clone repository")
            return 1
        
        # Test message creation and push
        test_message = "This is a test message"
        test_sender = "TestUser"
        
        # Create message file
        filepath = git_manager.create_message_file(test_message, test_sender)
        if not filepath:
            print("Failed to create message file")
            return 1
        
        # Push message
        commit_hash = git_manager.push_message(filepath)
        if not commit_hash:
            print("Failed to push message")
            return 1
            
        print(f"Successfully pushed message with commit hash: {commit_hash}")
        return 0
        
    except Exception as e:
        print(f"Error in main: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
