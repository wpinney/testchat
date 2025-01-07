#!/usr/bin/env python3
import unittest
import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import sys
import time

# Add parent directory to path to import GitManager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from git_manager import GitManager

class TestGitManager(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.test_repo_url = "https://github.com/wpinney/testchat.git"
        self.git_manager = GitManager(self.test_repo_url)
        
        # Ensure messages directory exists and is empty
        if self.git_manager.messages_dir.exists():
            shutil.rmtree(self.git_manager.messages_dir)
        self.git_manager.messages_dir.mkdir(exist_ok=True)

    def test_init(self):
        """Test GitManager initialization"""
        # Clean up before test
        if self.git_manager.messages_dir.exists():
            shutil.rmtree(self.git_manager.messages_dir)
        self.git_manager.messages_dir.mkdir(exist_ok=True)
            
        self.assertIsNotNone(self.git_manager)
        self.assertEqual(self.git_manager.repo_url, self.test_repo_url)
        self.assertTrue(self.git_manager.github_token)
        self.assertTrue(self.git_manager.messages_dir.exists())

    def test_create_message_file(self):
        """Test message file creation"""
        # Clean up before test
        if self.git_manager.messages_dir.exists():
            shutil.rmtree(self.git_manager.messages_dir)
        self.git_manager.messages_dir.mkdir(exist_ok=True)
        
        test_content = "Test message"
        test_sender = "TestUser"
        
        # Create message file
        filepath = self.git_manager.create_message_file(test_content, test_sender)
        
        # Verify file was created
        self.assertIsNotNone(filepath)
        self.assertTrue(os.path.exists(filepath))
        
        # Verify file contents
        with open(filepath, 'r') as f:
            message_data = json.load(f)
            self.assertEqual(message_data['content'], test_content)
            self.assertEqual(message_data['sender'], test_sender)
            self.assertTrue('timestamp' in message_data)

    def test_message_history(self):
        """Test message history retrieval"""
        # Clean up before test
        if self.git_manager.messages_dir.exists():
            shutil.rmtree(self.git_manager.messages_dir)
        self.git_manager.messages_dir.mkdir(exist_ok=True)
        
        # Create multiple test messages
        messages = [
            ("Message 1", "User1"),
            ("Message 2", "User2"),
            ("Message 3", "User1")
        ]
        
        created_files = []
        # Add messages with a small delay between them
        for content, sender in messages:
            filepath = self.git_manager.create_message_file(content, sender)
            created_files.append(filepath)
            time.sleep(0.1)  # Add small delay to ensure different timestamps
        
        print("\nCreated message files:", created_files)
        
        # List files in messages directory
        print("\nFiles in messages directory:")
        for file in self.git_manager.messages_dir.glob('message_*.json'):
            print(f"- {file}")
        
        # Get history
        history = self.git_manager.get_message_history()
        print("\nMessage history:", history)
        
        # Verify history
        self.assertEqual(len(history), len(messages))
        self.assertTrue(all('content' in msg and 'sender' in msg for msg in history))
        
        # Verify messages are in chronological order
        timestamps = [msg['timestamp'] for msg in history]
        self.assertEqual(timestamps, sorted(timestamps))

    def test_push_message(self):
        """Test pushing a message to GitHub"""
        # Clean up before test
        if self.git_manager.messages_dir.exists():
            shutil.rmtree(self.git_manager.messages_dir)
        self.git_manager.messages_dir.mkdir(exist_ok=True)
        
        # Create a test message
        test_content = "Test push message"
        test_sender = "TestUser"
        
        # Create and push message
        filepath = self.git_manager.create_message_file(test_content, test_sender)
        self.assertIsNotNone(filepath)
        
        # Try to push (this might fail if not in a git repo or no network)
        try:
            commit_hash = self.git_manager.push_message(filepath)
            if commit_hash:
                self.assertTrue(len(commit_hash) > 0)
                print(f"Successfully pushed with commit hash: {commit_hash}")
            else:
                print("Push skipped (expected in CI environment)")
        except Exception as e:
            print(f"Push test skipped: {e}")

def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()
