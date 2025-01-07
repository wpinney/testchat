-- Messages table schema
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    git_hash TEXT,  -- Store the Git commit hash for version tracking
    sender TEXT NOT NULL,
    is_synced BOOLEAN DEFAULT 0  -- Track if message has been synced to Git
);
