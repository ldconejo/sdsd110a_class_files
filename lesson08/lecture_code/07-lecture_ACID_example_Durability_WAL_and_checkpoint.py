import sqlite3

# Enable WAL mode
conn = sqlite3.connect("durability_example.db")
conn.execute("PRAGMA journal_mode=WAL;") # Enable Write-Ahead Logging
conn.execute("CREATE TABLE IF NOT EXISTS accounts(id INTEGER PRIMARY KEY, balance INTEGER);")
conn.execute("DELETE FROM accounts;") # Clear existing data
conn.execute("INSERT INTO accounts(id, balance) VALUES (1, 100);")
conn.commit()
print("Database initialized in WAL mode.")
conn.close()

# Simulate a transaction
conn = sqlite3.connect("durability_example.db")
conn.execute("BEGIN;") # Start transaction
conn.execute("UPDATE accounts SET balance = balance + 50 WHERE id = 1;")
conn.commit()  # This commit writes to WAL first, ensuring durability
print("Transaction committed; durable in WAL.")
conn.close()

# Manual checkpoint (flush WAL to main database)
conn = sqlite3.connect("durability_example.db")
conn.execute("PRAGMA wal_checkpoint(FULL);")
print("Checkpoint done: WAL flushed to main database file.")
conn.close()
