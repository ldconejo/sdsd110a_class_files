import threading
import json
import os
from abc import ABC, abstractmethod

# Simple interface (SOLID: ISP - small, focused interface)
class ConfigSource(ABC):
    @abstractmethod
    def load_config(self) -> dict:
        """Load configuration and return as dictionary."""
        pass

# Concrete Config Sources (SRP)
class FileConfigSource(ConfigSource):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_config(self) -> dict:
        """Load configuration from a JSON file, handle missing file gracefully."""
        if not os.path.exists(self.filepath):
            print(f"Warning: Config file not found: {self.filepath}")
            return {}
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error reading config file {self.filepath}: {e}")
            return {}

class EnvConfigSource(ConfigSource):
    def load_config(self) -> dict:
        """Load environment variables as configuration."""
        # Return all environment variables as config
        return dict(os.environ)

# Factory Pattern (SRP, OCP)
class ConfigSourceFactory:
    @staticmethod
    def create_source(source_type, *args) -> ConfigSource:
        if source_type == "file":
            return FileConfigSource(args[0])
        elif source_type == "env":
            return EnvConfigSource()
        else:
            raise ValueError(f"Unknown config source type: {source_type}")

# Singleton Config Manager (SRP, DIP)
class ConfigManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if ConfigManager._instance is not None:
            raise Exception("Use get_instance() method")
        self._config_data = {}
        self._factory = ConfigSourceFactory()  # DIP: factory dependency

    @classmethod
    def get_instance(cls):
        """Thread-safe singleton with lazy initialization."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = cls()
        return cls._instance

    def add_source(self, source_type, *args):
        """Create source via factory and update config data."""
        source = self._factory.create_source(source_type, *args)
        new_config = source.load_config()
        self._config_data.update(new_config)  # Later source overrides earlier ones

    def get(self, key, default=None):
        """Fetch a config key with optional default."""
        return self._config_data.get(key, default)

    def get_all(self) -> dict:
        """Return a safe copy of config data."""
        return dict(self._config_data)
