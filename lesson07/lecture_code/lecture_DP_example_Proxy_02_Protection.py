import time

class SecureResource:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self.sensitive_data = f"CONFIDENTIAL: Resource {resource_id} data"
    
    def read_data(self):
        return self.sensitive_data
    
    def write_data(self, new_data):
        self.sensitive_data = new_data
    
    def delete(self):
        print(f"🗑️  Resource {self.resource_id} deleted")

class SecurityProxy:
    def __init__(self, resource: SecureResource, user_role: str):
        self._resource = resource
        self.user_role = user_role
        self.access_log = []
    
    def _log_access(self, operation):
        """Log access attempts"""
        timestamp = time.time()
        self.access_log.append({
            "operation": operation,
            "user_role": self.user_role,
            "timestamp": timestamp,
            "resource_id": self._resource.resource_id
        })
        print(f"📝 ACCESS LOG: {self.user_role} performed {operation}")
    
    def read_data(self):
        """Read with access control"""
        self._log_access("READ")
        
        if self.user_role in ["admin", "user", "guest"]:
            return self._resource.read_data()
        else:
            raise PermissionError("Insufficient permissions to read")
    
    def write_data(self, new_data):
        """Write with access control"""
        self._log_access("WRITE")
        
        if self.user_role in ["admin", "user"]:
            return self._resource.write_data(new_data)
        else:
            raise PermissionError("Insufficient permissions to write")
    
    def delete(self):
        """Delete with access control"""
        self._log_access("DELETE")
        
        if self.user_role == "admin":
            return self._resource.delete()
        else:
            raise PermissionError("Only admins can delete resources")
    
    def get_access_log(self):
        """Get access log (admin only)"""
        if self.user_role == "admin":
            return self.access_log
        else:
            raise PermissionError("Only admins can view access logs")

if __name__ == "__main__":
    # Usage
    resource = SecureResource("SECRET_001")

    # Different user roles
    admin_proxy = SecurityProxy(resource, "admin")
    user_proxy = SecurityProxy(resource, "user")
    guest_proxy = SecurityProxy(resource, "guest")

    # Admin can do everything
    admin_proxy.read_data()
    admin_proxy.write_data("Updated by admin")
    print("Admin access log:", len(admin_proxy.get_access_log()))

    # User can read and write
    user_proxy.read_data()
    user_proxy.write_data("Updated by user")

    # Guest can only read
    guest_proxy.read_data()
    try:
        guest_proxy.write_data("Attempted by guest")  # Will fail
    except PermissionError as e:
        print(f"❌ {e}")
