import json
import os
import copy

DB_FILE = "database.json"
WAL_FILE = "wal.log"

# Initialize database if not exists
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"accounts": {"A": 1000, "B": 500}}, f)

# Load database
with open(DB_FILE, "r") as f:
    db = json.load(f)

# --- WAL Handling ---
def write_ahead_log(transaction):
    """Append transaction to WAL for durability."""
    with open(WAL_FILE, "a") as f:
        f.write(json.dumps(transaction) + "\n")
    print("WAL written:", transaction["transaction_id"])

def replay_wal():
    """Replay WAL on startup to restore any uncommitted transactions."""
    global db
    if not os.path.exists(WAL_FILE):
        return
    print("Replaying WAL...")
    with open(WAL_FILE, "r") as f:
        for line in f:
            transaction = json.loads(line)
            try:
                apply_transaction(transaction)
            except Exception as e:
                print(f"Failed to apply transaction {transaction['transaction_id']} during recovery:", e)
    # After replay, truncate WAL
    open(WAL_FILE, "w").close()
    # Persist recovered DB
    with open(DB_FILE, "w") as f:
        json.dump(db, f)
    print("WAL replay complete.\n")

# --- Transaction Handling ---
def apply_transaction(transaction):
    """Apply transaction to in-memory DB, may raise error."""
    for action in transaction["actions"]:
        account_id = action["account_id"]
        change = action["change"]
        db["accounts"][account_id] += change
        if db["accounts"][account_id] < 0:
            raise ValueError(f"Insufficient funds in account {account_id}!")
    print("Transaction applied:", transaction["transaction_id"])

def commit(transaction):
    """Commit a transaction safely with WAL and rollback."""
    global db
    db_snapshot = copy.deepcopy(db)
    try:
        # 1. Write to WAL
        write_ahead_log(transaction)

        # 2. Apply transaction
        apply_transaction(transaction)

        # 3. Persist DB
        with open(DB_FILE, "w") as f:
            json.dump(db, f)
        print("Transaction committed!\n")

    except Exception as e:
        db = db_snapshot
        print("Transaction failed! Rolled back.", e)

# --- Startup Recovery ---
replay_wal()

# --- Example Transactions ---
transaction_1 = {
    "transaction_id": "T1",
    "actions": [
        {"account_id": "A", "change": -300},
        {"account_id": "B", "change": 300}
    ]
}

transaction_2 = {
    "transaction_id": "T2",
    "actions": [
        {"account_id": "A", "change": -2000},  # Not enough funds
        {"account_id": "B", "change": 2000}
    ]
}

commit(transaction_1)  # should succeed
commit(transaction_2)  # should fail and rollback

print("Final DB state:", db)
