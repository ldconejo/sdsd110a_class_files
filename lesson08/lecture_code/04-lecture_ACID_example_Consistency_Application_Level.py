import sqlite3

# Connect to SQLite (in-memory for demo)
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create accounts table
cursor.execute("""
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    owner TEXT NOT NULL,
    balance REAL NOT NULL CHECK (balance >= 0)
)
""")

# Insert sample accounts
cursor.execute("INSERT INTO accounts VALUES (1, 'Alice', 5000)")
cursor.execute("INSERT INTO accounts VALUES (2, 'Bob', 3000)")

conn.commit()

# --- Application-level consistency: transfer function ---
def transfer_funds(from_id, to_id, amount):
    # Business rule: maximum transfer limit
    MAX_TRANSFER = 10000
    if amount > MAX_TRANSFER:
        raise ValueError(f"Transfer exceeds limit of ${MAX_TRANSFER}!")
    
    # Fetch balances
    cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (from_id,))
    from_balance = cursor.fetchone()[0]
    
    if from_balance < amount:
        raise ValueError("Insufficient funds!")
    
    # Apply transaction
    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_id = ?", (amount, from_id))
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_id = ?", (amount, to_id))
    conn.commit()
    print(f"Transferred ${amount} from account {from_id} to {to_id}.")

# --- Test transfers ---
transfer_funds(1, 2, 2000)  # ✅ Valid
try:
    transfer_funds(1, 2, 15000)  # ❌ Exceeds limit
except ValueError as e:
    print("Failed:", e)

# Check final balances
cursor.execute("SELECT * FROM accounts")
print(cursor.fetchall())
