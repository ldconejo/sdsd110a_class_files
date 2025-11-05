# Test environment variables
import os
os.environ['LOG_LEVEL'] = 'INFO'
os.environ['VERSION'] = '1.0'
from hw_config_manager_solution import ConfigManager

# Test your code
config = ConfigManager.get_instance()
config.add_source("file", "hw_config.json")  # Factory creates FileConfigSource
config.add_source("env")                  # Factory creates EnvConfigSource

print("=== Configuration Test ===")
print(f"App name: {config.get('app_name')}")
print(f"Debug: {config.get('debug')}")
print(f"Log level: {config.get('LOG_LEVEL')}")
print(f"Version: {config.get('VERSION')}")

# Test singleton
config2 = ConfigManager.get_instance()
print(f"Same instance: {config is config2}")  # Should be True
