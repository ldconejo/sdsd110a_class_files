📦 Created connection pool (max: 3)
Initial stats: {'available': 0, 'total_created': 0, 'max_connections': 3}

📥 Getting connections from pool:
🔗 Creating new database connection...
🔗 Creating new database connection...
Stats after getting 2: {'available': 0, 'total_created': 2, 'max_connections': 3}
Query result: Connection 1234: Result for 'SELECT * FROM users'

📤 Returning connections to pool:
📤 Returned connection 1234 to pool
📤 Returned connection 5678 to pool
Stats after returning: {'available': 2, 'total_created': 2, 'max_connections': 3}

♻️ Testing connection reuse:
♻️ Reusing connection 5678
Reused connection result: Connection 5678: Result for 'SELECT * FROM products'
📤 Returned connection 5678 to pool

=== Performance Comparison ===
🐌 Without pool (creating new connections):
🔗 Creating new database connection...
🔗 Creating new database connection...
🔗 Creating new database connection...
🔗 Creating new database connection...
🔗 Creating new database connection...
Time without pool: 1.05 seconds

🚀 With pool (reusing connections):
📦 Created connection pool (max: 3)
🔗 Creating new database connection...
♻️ Reusing connection 9012
♻️ Reusing connection 9012
♻️ Reusing connection 9012
♻️ Reusing connection 9012
Time with pool: 0.25 seconds

🎉 Pool was 76.2% faster!
