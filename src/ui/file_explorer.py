# src/ui/file_explorer.py

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QTreeWidget, QTreeWidgetItem, QLabel, QMenu, QAction, QMessageBox
)
from PyQt5.QtCore import Qt

class FileExplorer(QWidget):
    """Improved File Explorer with dynamic search and optimized folder loading."""
    def __init__(self, open_file_callback):
        super().__init__()
        self.open_file_callback = open_file_callback

        # Search bar for filtering files and folders
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search files...")
        self.search_bar.textChanged.connect(self.filter_tree)

        # Tree widget to display files and folders
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)  # Hide the header for simplicity
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_context_menu)
        self.tree.itemDoubleClicked.connect(self.open_item)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(QLabel("File Explorer"))
        layout.addWidget(self.search_bar)
        layout.addWidget(self.tree)
        self.setLayout(layout)

        # Load the initial directory structure
        self.load_directory(".")

    def load_directory(self, path):
        """Load the root directory into the tree."""
        self.tree.clear()  # Clear the tree before loading
        root_item = QTreeWidgetItem(self.tree, [os.path.basename(path)])
        root_item.setData(0, Qt.UserRole, path)  # Store the full path
        self.add_children(root_item, path)  # Add child files/folders recursively
        root_item.setExpanded(True)  # Expand the root folder

    def add_children(self, parent_item, path):
        """Recursively add child files and folders."""
        try:
            for entry in sorted(os.listdir(path)):
                entry_path = os.path.join(path, entry)
                child_item = QTreeWidgetItem(parent_item, [entry])
                child_item.setData(0, Qt.UserRole, entry_path)

                if os.path.isdir(entry_path):
                    # Mark as expandable but don't load children yet (for lazy loading)
                    child_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
                else:
                    child_item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)
        except PermissionError:
            # Handle cases where the program doesn't have permission to access a folder
            QMessageBox.warning(self, "Permission Denied", f"Cannot access: {path}")

    def open_item(self, item, column):
        """Handle double-clicks to open files or load folders."""
        full_path = item.data(0, Qt.UserRole)

        if os.path.isdir(full_path):
            # If the folder isn't loaded yet, load it dynamically
            if item.childCount() == 0:
                self.add_children(item, full_path)
            item.setExpanded(not item.isExpanded())  # Toggle expansion
        else:
            # If it's a file, open it
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                    self.open_file_callback(full_path, content)
            except FileNotFoundError:
                QMessageBox.warning(self, "Error", f"File not found: {full_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def open_context_menu(self, position):
        """Open the context menu with file operations."""
        item = self.tree.itemAt(position)
        if item:
            menu = QMenu(self)
            open_action = QAction("Open", self)
            open_action.triggered.connect(lambda: self.open_item(item, 0))
            menu.addAction(open_action)
            menu.exec_(self.tree.viewport().mapToGlobal(position))

    def filter_tree(self):
        """Filter the tree view based on search input."""
        search_text = self.search_bar.text().lower()
        root = self.tree.invisibleRootItem()
        self._filter_items(root, search_text)

    def _filter_items(self, parent_item, search_text):
        """Recursively filter tree items based on search input."""
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            item_text = child.text(0).lower()
            match = search_text in item_text

            # Show or hide the item based on the search match
            child.setHidden(not match)
            if not match:
                self._filter_items(child, search_text)  # Continue filtering children
