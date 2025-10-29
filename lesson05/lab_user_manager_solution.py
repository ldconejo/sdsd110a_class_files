import re
import json

# ================================================================
# USER VALIDATOR
# ================================================================
# SRP FIX: This class now handles *only validation logic*.
# It knows NOTHING about files, emails, or logging.
# ================================================================
class UserValidator:
    @staticmethod
    def validate_email(email):
        """Check if email matches valid format"""
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

    @staticmethod
    def validate_age(age):
        """Check if user is 18 or older"""
        return age >= 18


# ================================================================
# USER REPOSITORY
# ================================================================
# SRP FIX: Handles *only persistence* of users (loading/saving).
# DIP FIX: UserManager will depend on this *through abstraction*,
# not by directly calling `open()` or `json.dump()`.
# ================================================================
class UserRepository:
    def __init__(self, filepath="users.json"):
        self.filepath = filepath
        self.users = self.load_users()

    def load_users(self):
        """Load users from file"""
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_users(self):
        """Save users to file"""
        with open(self.filepath, "w") as f:
            json.dump(self.users, f)

    def add_user(self, user):
        """Add user to in-memory list and persist to file"""
        self.users.append(user)
        self.save_users()


# ================================================================
# EMAIL SERVICE
# ================================================================
# SRP FIX: Handles *only email-related operations*.
# DIP FIX: Injected into UserManager, so you can swap
# a different email sender (SMTP, API, etc.) without changing it.
# ================================================================
class EmailService:
    @staticmethod
    def send_welcome_email(email):
        print(f"Welcome email sent to {email}")


# ================================================================
# LOGGER
# ================================================================
# SRP FIX: Handles *only logging*.
# DIP FIX: Can be replaced by a different logging implementation
# (e.g., file logger, monitoring system, etc.)
# ================================================================
class Logger:
    @staticmethod
    def log(message):
        print(f"[LOG] {message}")


# ================================================================
# USER MANAGER (High-Level Module)
# ================================================================
# SRP FIX: Handles only the *workflow* of user creation.
# It delegates validation, persistence, email, and logging.
#
# DIP FIX: UserManager depends on *abstracted dependencies*
# (validator, repository, email_service, logger)
# passed via constructor — not on hardcoded implementations.
# ================================================================
class UserManager:
    def __init__(self, validator, repository, email_service, logger):
        # Dependencies are *injected* instead of hardcoded
        self.validator = validator
        self.repository = repository
        self.email_service = email_service
        self.logger = logger

    def create_user(self, name, email, age):
        """Create and store a user using injected services"""

        # --- Validation responsibility (delegated) ---
        if not self.validator.validate_email(email):
            self.logger.log("Invalid email address")
            return False
        if not self.validator.validate_age(age):
            self.logger.log("User must be 18 or older")
            return False

        # --- Repository responsibility (delegated) ---
        user = {"id": len(self.repository.users) + 1, "name": name, "email": email, "age": age}
        self.repository.add_user(user)

        # --- Email responsibility (delegated) ---
        self.email_service.send_welcome_email(email)

        # --- Logging responsibility (delegated) ---
        self.logger.log(f"User {name} created successfully")

        return True


# ================================================================
# 🧪 USAGE EXAMPLE
# ================================================================
# DIP: Inject dependencies explicitly.
# If you want a database repository or SMTP emailer later,
# just pass those classes — no changes to UserManager needed!
# ================================================================
if __name__ == "__main__":
    validator = UserValidator()
    repository = UserRepository()
    email_service = EmailService()
    logger = Logger()

    user_manager = UserManager(validator, repository, email_service, logger)

    user_manager.create_user("John Doe", "john@example.com", 25)
    user_manager.create_user("Jane Smith", "invalid-email", 17)