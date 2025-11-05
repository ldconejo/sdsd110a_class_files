import threading
import json
import os

from abc import ABC, abstractmethod

# Simple interface (SOLID: ISP - small, focused interface)
class ConfigSource(ABC):
    @abstractmethod
    def load_config(self):
        """Load configuration and return as dictionary"""
        pass

class FileConfigSource(ConfigSource):
    def __init__(self, filepath):
        self.filepath = filepath

    def load_config(self):
        # TODO: Load JSON file and return dictionary
        # Handle file not found gracefully
        pass

class EnvConfigSource(ConfigSource):
    def load_config(self):
        # TODO: Return environment variables as dictionary
        # You can return all env vars or filter specific ones
        pass

class ConfigSourceFactory:
    @staticmethod
    def create_source(source_type, *args):
        """Simple factory to create config sources"""
        if source_type == "file":
            # args[0] should be the filepath
            return FileConfigSource(args[0])
        elif source_type == "env":
            return EnvConfigSource()
        else:
            raise ValueError(f"Unknown source type: {source_type}")

class ConfigManager:
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        if ConfigManager._instance is not None:
            raise Exception("Use get_instance() method")
        self._config_data = {}
        self._factory = ConfigSourceFactory()  # Factory for creating sources
    
    @classmethod
    def get_instance(cls):
        # TODO: Implement basic thread-safe singleton
        # Use the lock to ensure only one instance is created
        pass
    
    def add_source(self, source_type, *args):
        # TODO: Use factory to create config source
        # TODO: Load config from source and add to self._config_data
        pass
    
    def get(self, key, default=None):
        # TODO: Return value from self._config_data or default
        pass
    
    def get_all(self):
        # TODO: Return copy of all configuration data
        pass
