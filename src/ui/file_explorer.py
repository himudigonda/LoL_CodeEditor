# src/ui/file_explorer.py

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView, QFileSystemModel

class FileExplorer(QWidget):
    """File Explorer to browse and open files."""
    def __init__(self, open_file_callback):
        super().__init__()
        self.open_file_callback = open_file_callback

        # File system model
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())

        # Tree view for displaying files
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(os.getcwd()))
        self.tree.doubleClicked.connect(self.open_file)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def open_file(self, index):
        """Handle file opening from the explorer."""
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                self.open_file_callback(file_path, content)
