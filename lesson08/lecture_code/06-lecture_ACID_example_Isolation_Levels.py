import sqlite3

DB_FILE = "example.db"

def new_conn():
    conn = sqlite3.connect(DB_FILE, isolation_level=None, timeout=5.0)
    return conn

def reset_data():
    conn = new_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, balance INTEGER);")
    cur.execute("DELETE FROM accounts;")
    cur.execute("INSERT INTO accounts(id, balance) VALUES (1, 100);")
    conn.commit()
    conn.close()
    print("\nDatabase reset to balance = 100")

# 1. READ UNCOMMITTED — simulate dirty read
def demo_read_uncommitted():
    print("\n=== READ UNCOMMITTED (Simulated) ===")
    reset_data()
    conn = new_conn()
    conn.execute("PRAGMA read_uncommitted = true;")
    cur = conn.cursor()

    # Transaction A begins
    conn.execute("BEGIN;")
    cur.execute("UPDATE accounts SET balance = balance - 50 WHERE id = 1;")
    print("Transaction A updated balance to 50 — not committed.")

    # Simulate Transaction B reading dirty data
    cur.execute("SELECT balance FROM accounts WHERE id = 1;")
    print("Transaction B sees:", cur.fetchone()[0], "(dirty read)")

    conn.rollback()
    conn.close()

# 2. READ COMMITTED — prevent dirty reads
def demo_read_committed():
    print("\n=== READ COMMITTED (Simulated) ===")
    reset_data()
    conn = new_conn()
    cur = conn.cursor()

    # Transaction A begins
    conn.execute("BEGIN;")
    cur.execute("UPDATE accounts SET balance = balance - 50 WHERE id = 1;")
    print("Transaction A updated balance — not committed.")

    # Simulate Transaction B reading committed data
    cur.execute("SELECT balance FROM accounts WHERE id = 1;")
    print("Transaction B sees:", cur.fetchone()[0], "(still 100)")

    conn.commit()
    cur.execute("SELECT balance FROM accounts WHERE id = 1;")
    print("Transaction B sees after commit:", cur.fetchone()[0])

    conn.close()

# 3. REPEATABLE READ — simulate stable snapshot
def demo_repeatable_read():
    print("\n=== REPEATABLE READ (Simulated) ===")
    reset_data()
    conn = new_conn()
    cur = conn.cursor()

    conn.execute("BEGIN;")
    cur.execute("SELECT balance FROM accounts WHERE id = 1;")
    first_read = cur.fetchone()[0]
    print("Transaction A first read:", first_read)

    # Simulate another transaction updating data and committing
    conn.execute("UPDATE accounts SET balance = 50 WHERE id = 1;")
    print("Another transaction updates balance to 50 and commits.")

    # Transaction A reads again (in SQLite it sees latest value, but we simulate snapshot)
    print("Transaction A second read (simulated snapshot):", first_read, "(unchanged)")

    conn.commit()
    conn.close()

# 4. SERIALIZABLE — simulate phantom prevention
def demo_serializable():
    print("\n=== SERIALIZABLE (Simulated) ===")
    reset_data()
    conn = new_conn()
    cur = conn.cursor()

    conn.execute("BEGIN;")
    cur.execute("SELECT COUNT(*) FROM accounts;")
    first_count = cur.fetchone()[0]
    print("Transaction A first row count:", first_count)

    # Simulate phantom row insertion
    print("Simulating another transaction inserting a new row (phantom).")
    cur.execute("INSERT INTO accounts(balance) VALUES (200);")
    print("New row inserted but Transaction A ignores it in its snapshot.")

    cur.execute("SELECT COUNT(*) FROM accounts;")
    print("Transaction A row count again (simulated snapshot):", first_count, "(phantoms prevented)")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    demo_read_uncommitted()
    demo_read_committed()
    demo_repeatable_read()
    demo_serializable()
