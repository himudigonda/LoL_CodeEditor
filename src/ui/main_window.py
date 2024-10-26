# src/ui/main_window.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QTextEdit, QAction, QFileDialog, QVBoxLayout, QWidget
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LightCode - AI-powered Code Editor")
        self.setGeometry(100, 100, 800, 600)

        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add menu bar
        self._create_menu()

    def _create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        # Add 'Open File' action
        open_file_action = QAction("Open File", self)
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        # Add 'Exit' action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        # Open file dialog to select a file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)

        if file_name:
            with open(file_name, 'r') as file:
                content = file.read()
                self._add_tab(file_name, content)

    def _add_tab(self, title, content):
        # Create a new text editor widget for the file
        editor = QTextEdit()
        editor.setText(content)

        # Add a new tab with the editor
        self.tabs.addTab(editor, title)

def run_editor():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_editor()
