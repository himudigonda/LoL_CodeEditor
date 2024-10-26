import json
import os

class SettingsManager:
    """Manage editor settings."""
    def __init__(self, config_path="config/settings.json"):
        self.config_path = config_path
        self.settings = self.load_settings()

    def load_settings(self):
        """Load settings from JSON."""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {}

    def save_settings(self, new_settings):
        """Save settings to JSON."""
        self.settings.update(new_settings)
        with open(self.config_path, "w") as f:
            json.dump(self.settings, f, indent=4)
