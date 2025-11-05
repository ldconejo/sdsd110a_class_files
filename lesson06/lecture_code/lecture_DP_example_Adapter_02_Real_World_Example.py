# Your application expects this interface
class DatabaseConnection:
    def connect(self, connection_string):
        pass
    
    def execute_query(self, query):
        pass
    
    def close(self):
        pass

# Third-party library has different interface
class MySQLConnector:
    def establish_connection(self, host, user, password, database):
        print(f"Connected to MySQL: {database}@{host}")
        return True
    
    def run_sql(self, sql_statement):
        return f"MySQL result for: {sql_statement}"
    
    def disconnect(self):
        print("MySQL connection closed")

# Adapter makes third-party library compatible
class MySQLAdapter(DatabaseConnection):
    def __init__(self):
        self.mysql_connector = MySQLConnector()
        self.is_connected = False
    
    def connect(self, connection_string):
        # Parse connection string: "mysql://user:pass@host/db"
        parts = connection_string.replace("mysql://", "").split("/")
        user_host = parts[0].split("@")
        user_pass = user_host[0].split(":")
        
        self.is_connected = self.mysql_connector.establish_connection(
            user_host[1], user_pass[0], user_pass[1], parts[1]
        )
        return self.is_connected
    
    def execute_query(self, query):
        if self.is_connected:
            return self.mysql_connector.run_sql(query)
        return None
    
    def close(self):
        self.mysql_connector.disconnect()
        self.is_connected = False

# Your application code doesn't change
def backup_data(db: DatabaseConnection):
    db.connect("mysql://admin:secret@localhost/myapp")
    result = db.execute_query("SELECT * FROM users")
    db.close()
    return result

if __name__ == "__main__":
    # Works with any database through adapters
    mysql_db = MySQLAdapter()
    backup_data(mysql_db)
