import re
import json

class UserManager:
    def __init__(self):
        self.users = []
    
    def create_user(self, name, email, age):
        # Email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            print("Invalid email address")
            return False
        
        # Age validation
        if age < 18:
            print("User must be 18 or older")
            return False
        
        # Create user
        user = {
            "id": len(self.users) + 1,
            "name": name,
            "email": email,
            "age": age
        }
        
        # Save to file
        self.users.append(user)
        with open("users.json", "w") as f:
            json.dump(self.users, f)
        
        # Send welcome email (simulated)
        print(f"Welcome email sent to {email}")
        
        # Log activity
        print(f"User {name} created successfully")
        
        return True
    
    def get_all_users(self):
        return self.users

# Usage example
user_manager = UserManager()
user_manager.create_user("John Doe", "john@example.com", 25)
user_manager.create_user("Jane Smith", "invalid-email", 17)
