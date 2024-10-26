# src/ui/main_window.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QTextEdit, QAction, QFileDialog,
    QVBoxLayout, QWidget, QSplitter, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LightCode - AI-powered Code Editor")
        self.setGeometry(100, 100, 1000, 600)

        # Create a horizontal splitter to divide editor and chat
        splitter = QSplitter(Qt.Horizontal)

        # Tabs for multiple files (left pane)
        self.tabs = QTabWidget()
        splitter.addWidget(self.tabs)

        # Chat UI placeholder (right pane)
        self.chat_ui = QLabel("Chat Interface - Coming Soon!")
        self.chat_ui.setAlignment(Qt.AlignCenter)
        splitter.addWidget(self.chat_ui)

        # Set proportions: editor expands more than chat
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        # Set the central widget to the splitter
        self.setCentralWidget(splitter)

        # Add menu and status bar
        self._create_menu()
        self.status_bar = self.statusBar()

    def _create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        # Open File action
        open_file_action = QAction("Open File", self)
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        # Save File action
        save_file_action = QAction("Save File", self)
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        # Save As action
        save_as_action = QAction("Save As...", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)

        if file_name:
            with open(file_name, 'r') as file:
                content = file.read()
                self._add_tab(file_name, content)

    def save_file(self):
        current_widget = self.tabs.currentWidget()
        if current_widget and isinstance(current_widget, QTextEdit):
            file_name = self.tabs.tabText(self.tabs.currentIndex())
            if file_name.startswith("Untitled"):
                self.save_file_as()
            else:
                with open(file_name, 'w') as file:
                    file.write(current_widget.toPlainText())

    def save_file_as(self):
        current_widget = self.tabs.currentWidget()
        if current_widget and isinstance(current_widget, QTextEdit):
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "All Files (*)", options=options)

            if file_name:
                with open(file_name, 'w') as file:
                    file.write(current_widget.toPlainText())
                self.tabs.setTabText(self.tabs.currentIndex(), file_name)

    def _add_tab(self, title, content):
        editor = QTextEdit()
        editor.setText(content)

        # Connect to cursor position update
        editor.cursorPositionChanged.connect(lambda: self.update_status(editor))

        self.tabs.addTab(editor, title)
        self.tabs.setCurrentWidget(editor)

    def update_status(self, editor):
        cursor = editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.status_bar.showMessage(f"Line: {line}, Column: {col}")

def run_editor():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_editor()
