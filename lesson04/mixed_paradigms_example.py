import json
# Web application mixing paradigms 

# OOP for resource management 
class DatabasePool: 
    def __init__(self,connection_string): 
        self.connections = [] 
        self.connection_string = connection_string 

    def get_connection(self): 
        # Return pooled connection 
        pass 

# Functional for data processing 
def transform_user_data(users): 
	return list(map( 
		lambda user: {
			**user, 
			'full_name': f"{user['first']} {user['last']}", 
			'display_name': user['first'].upper() 
		}, 
		filter(lambda user: user['active'],users) 
	)) 

# Event-driven for handling requests 
async def handle_user_request(request): 
	db = DatabasePool("postgresql://localhost")  # OOP 
	users = db.query("SELECT * FROM users")  # Procedural call 
	processed = transform_user_data(users)  # Functional 
	return json.dumps(processed)  # Result


