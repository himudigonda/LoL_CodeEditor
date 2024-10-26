# src/ui/main_window.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QSplitter, QStatusBar, QStyleFactory,
    QFileDialog, QAction, QToolBar, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize
from src.ui.editor import CodeEditor
from src.ui.chat_ui import ChatUI
from src.ui.file_explorer import FileExplorer

class MainWindow(QMainWindow):
    """Main window for the code editor."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LightCode - AI-powered Code Editor")
        self.setGeometry(100, 100, 1600, 900)

        # Horizontal splitter for layout
        splitter = QSplitter(Qt.Horizontal)

        # Add File Explorer
        self.file_explorer = FileExplorer(self._add_tab)
        splitter.addWidget(self.file_explorer)

        # Tabbed editor pane
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        splitter.addWidget(self.tabs)

        # Add Chat UI
        chat_widget = ChatUI()
        splitter.addWidget(chat_widget)

        # Set better pane ratios
        splitter.setStretchFactor(0, 1)  # File Explorer (20%)
        splitter.setStretchFactor(1, 5)  # Editor (70%)
        splitter.setStretchFactor(2, 1)  # Chat Pane (10%)

        self.setCentralWidget(splitter)

        # Add toolbar, menu, and status bar
        self._create_toolbar()
        self._create_menu()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self._update_status_bar("", 0, 0)

        self.setStyle(QStyleFactory.create("Fusion"))

    def _create_toolbar(self):
        """Creates the toolbar with actions."""
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setIconSize(QSize(24, 24))

        open_action = QAction(QIcon("assets/icons/open.png"), "Open", self)
        open_action.triggered.connect(self.open_file)

        save_action = QAction(QIcon("assets/icons/save.png"), "Save", self)
        save_action.triggered.connect(self.save_file)

        theme_action = QAction(QIcon("assets/icons/theme.png"), "Toggle Theme", self)
        theme_action.triggered.connect(self.toggle_theme)

        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addAction(theme_action)

        self.addToolBar(toolbar)

    def _create_menu(self):
        """Creates the menu bar."""
        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        """Open a file and display it in a new tab."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                content = f.read()
                self._add_tab(file_name, content)

    def save_file(self):
        """Save the current file."""
        current_widget = self.tabs.currentWidget()
        if current_widget:
            editor = current_widget.layout().itemAt(0).widget()
            with open(self.tabs.tabText(self.tabs.currentIndex()), 'w') as f:
                f.write(editor.toPlainText())

    def _add_tab(self, title, content):
        """Add a new tab with the given content."""
        editor = CodeEditor()
        editor.setPlainText(content)
        editor.textChanged.connect(lambda: self._update_status_bar(title, editor.blockCount(), len(editor.toPlainText())))

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(editor)
        container.setLayout(layout)

        self.tabs.addTab(container, title)
        self.tabs.setCurrentWidget(container)

    def close_tab(self, index):
        """Close the tab at the given index."""
        self.tabs.removeTab(index)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.style().objectName() == "Fusion":
            self.setStyle(QStyleFactory.create("Windows"))
        else:
            self.setStyle(QStyleFactory.create("Fusion"))

    def _update_status_bar(self, file_name, line_count, word_count):
        """Update the status bar with file and text stats."""
        self.status_bar.showMessage(f"File: {file_name} | Lines: {line_count} | Words: {word_count}")

def run_editor():
    """Run the editor application."""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_editor()
