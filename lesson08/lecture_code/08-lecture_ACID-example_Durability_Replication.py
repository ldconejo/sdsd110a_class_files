import sqlite3
import shutil
import os

PRIMARY_DB = "primary.db"
REPLICA_DB = "replica.db"

# Clean up old files
for db in [PRIMARY_DB, REPLICA_DB]:
    if os.path.exists(db):
        os.remove(db)

# Initialize primary
conn = sqlite3.connect(PRIMARY_DB)
conn.execute("CREATE TABLE accounts(id INTEGER PRIMARY KEY, balance INTEGER);")
conn.execute("INSERT INTO accounts(id, balance) VALUES (1, 100);")
conn.commit()
conn.close()
print("Primary database initialized.")

# Simulate replication function
def replicate():
    """Copy primary to replica to simulate synchronous replication."""
    shutil.copyfile(PRIMARY_DB, REPLICA_DB)
    print("Replica updated.")

# Transaction on primary
conn = sqlite3.connect(PRIMARY_DB)
conn.execute("BEGIN;")
conn.execute("UPDATE accounts SET balance = balance + 50 WHERE id = 1;")
print("Transaction committed on primary (not yet replicated).")
conn.commit()

# Replicate to secondary
replicate()

# Verify primary
conn = sqlite3.connect(PRIMARY_DB)
cur = conn.cursor()
cur.execute("SELECT balance FROM accounts WHERE id = 1;")
print("Original balance:", cur.fetchone()[0])
conn.close()

# Verify replica
conn = sqlite3.connect(REPLICA_DB)
cur = conn.cursor()
cur.execute("SELECT balance FROM accounts WHERE id = 1;")
print("Replica balance:", cur.fetchone()[0])
conn.close()
