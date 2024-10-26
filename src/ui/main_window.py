# src/ui/main_window.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QSplitter, QStatusBar, QStyleFactory,
    QToolBar, QVBoxLayout, QWidget, QAction, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from src.ui.editor import CodeEditor
from src.ui.chat_ui import ChatUI
from src.ui.file_explorer import FileExplorer

class MainWindow(QMainWindow):
    """Main window for the LightCode editor."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LightCode - AI-powered Code Editor")
        self.setGeometry(100, 100, 1600, 900)

        # Set up the main layout with a splitter
        splitter = QSplitter(Qt.Horizontal)

        # Add the custom File Explorer
        self.file_explorer = FileExplorer(self._open_file_in_tab)
        self.file_explorer.setMaximumWidth(300)  # Limit explorer width
        splitter.addWidget(self.file_explorer)

        # Add the tabbed editor pane
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        splitter.addWidget(self.tabs)

        # Add the chat interface
        chat_widget = ChatUI()
        chat_widget.setMaximumWidth(300)  # Limit chat width
        splitter.addWidget(chat_widget)

        # Set pane ratios
        splitter.setStretchFactor(0, 2)  # File Explorer (small)
        splitter.setStretchFactor(1, 6)  # Editor Pane (large)
        splitter.setStretchFactor(2, 2)  # Chat Pane (small)
        self.setCentralWidget(splitter)

        # Add toolbar, menu, and status bar
        self._create_toolbar()
        self._create_menu()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.setStyle(QStyleFactory.create("Fusion"))

    def _create_toolbar(self):
        """Creates the toolbar with actions."""
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setIconSize(QSize(24, 24))

        open_action = QAction(QIcon("assets/icons/open.png"), "Open", self)
        open_action.triggered.connect(self.open_file_dialog)

        save_action = QAction(QIcon("assets/icons/save.png"), "Save", self)
        save_action.triggered.connect(self.save_file)

        close_all_action = QAction("Close All Tabs", self)
        close_all_action.triggered.connect(self.close_all_tabs)

        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addAction(close_all_action)
        self.addToolBar(toolbar)

    def _create_menu(self):
        """Creates the menu bar."""
        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

    def _open_file_in_tab(self, file_path, content):
        """Add a new tab with the file content."""
        editor = CodeEditor()
        editor.setPlainText(content)

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(editor)
        container.setLayout(layout)

        # Add the file to the tabs and set it as the current tab
        self.tabs.addTab(container, file_path)
        self.tabs.setCurrentWidget(container)
        self.status_bar.showMessage(f"Opened: {file_path}")

    def open_file_dialog(self):
        """Open a file via the system dialog."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    content = f.read()
                self._open_file_in_tab(file_name, content)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")

    def save_file(self):
        """Save the currently open file."""
        current_widget = self.tabs.currentWidget()
        if current_widget is not None:
            editor = current_widget.layout().itemAt(0).widget()
            file_name = self.tabs.tabText(self.tabs.currentIndex())

            try:
                with open(file_name, 'w') as f:
                    f.write(editor.toPlainText())
                self.status_bar.showMessage(f"Saved: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
        else:
            QMessageBox.warning(self, "No Tab Open", "Please open a file first.")

    def close_tab(self, index):
        """Close the tab at the specified index."""
        self.tabs.removeTab(index)
        if self.tabs.count() == 0:
            self.status_bar.showMessage("No files open")

    def close_all_tabs(self):
        """Close all open tabs."""
        self.tabs.clear()
        self.status_bar.showMessage("All tabs closed")

def run_editor():
    """Run the editor application."""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_editor()
