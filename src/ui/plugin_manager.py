# src/ui/plugin_manager.py

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton

class PluginManager(QWidget):
    """Plugin manager to load and display available plugins."""
    def __init__(self, plugin_folder="src/plugins"):
        super().__init__()
        self.plugin_folder = plugin_folder

        self.plugin_list = QListWidget()
        self.load_plugins()

        reload_button = QPushButton("Reload Plugins")
        reload_button.clicked.connect(self.load_plugins)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Plugins"))
        layout.addWidget(self.plugin_list)
        layout.addWidget(reload_button)
        self.setLayout(layout)

    def load_plugins(self):
        """Load plugins from the plugin folder."""
        self.plugin_list.clear()
        for root, _, files in os.walk(self.plugin_folder):
            for file in files:
                if file.endswith(".py"):
                    self.plugin_list.addItem(os.path.join(root, file))
