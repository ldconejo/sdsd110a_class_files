import sqlite3

# Connect to SQLite
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    stock INTEGER NOT NULL CHECK (stock >= 0)
)
""")

cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

# Insert sample product
cursor.execute("INSERT INTO products VALUES (1, 'Laptop', 5)")
conn.commit()

# --- Function to place an order with multi-table consistency ---
def place_order(product_id, quantity):
    try:
        # Start transaction
        conn.execute("BEGIN")

        # Check inventory
        cursor.execute("SELECT stock FROM products WHERE product_id = ?", (product_id,))
        stock = cursor.fetchone()[0]

        if stock < quantity:
            raise ValueError("Not enough inventory!")

        # Insert order
        cursor.execute("INSERT INTO orders (product_id, quantity) VALUES (?, ?)", (product_id, quantity))

        # Reduce inventory
        cursor.execute("UPDATE products SET stock = stock - ? WHERE product_id = ?", (quantity, product_id))

        # Commit transaction
        conn.commit()
        print(f"Order placed for {quantity} units of product {product_id}.")
    except Exception as e:
        # Rollback if anything goes wrong
        conn.rollback()
        print("Order failed, rolled back:", e)

# --- Test cases ---
place_order(1, 3)  # ✅ Success
place_order(1, 3)  # ❌ Fails (only 2 left)

# Check final state
cursor.execute("SELECT * FROM products")
print("Products:", cursor.fetchall())
cursor.execute("SELECT * FROM orders")
print("Orders:", cursor.fetchall())
