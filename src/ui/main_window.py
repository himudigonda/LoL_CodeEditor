# src/ui/main_window.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QSplitter, QStatusBar, QStyleFactory,
    QFileDialog, QAction, QToolBar, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize
from src.ui.editor import CodeEditor
from src.ui.chat_ui import ChatUI

class MainWindow(QMainWindow):
    """Main window for the code editor."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LightCode - AI-powered Code Editor")
        self.setGeometry(100, 100, 1600, 900)

        # Create a horizontal splitter
        splitter = QSplitter(Qt.Horizontal)

        # Add tabbed editor pane
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        splitter.addWidget(self.tabs)

        # Add chat UI
        chat_widget = ChatUI()
        splitter.addWidget(chat_widget)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

        # Add toolbar
        self._create_toolbar()

        # Add menu and status bar
        self._create_menu()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.setStyle(QStyleFactory.create("Fusion"))

    def _create_toolbar(self):
        """Creates the toolbar."""
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setIconSize(QSize(24, 24))

        open_action = QAction(QIcon("assets/icons/open.png"), "Open", self)
        open_action.triggered.connect(self.open_file)

        save_action = QAction(QIcon("assets/icons/save.png"), "Save", self)
        save_action.triggered.connect(self.save_file)

        exit_action = QAction(QIcon("assets/icons/exit.png"), "Exit", self)
        exit_action.triggered.connect(self.close)

        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addAction(exit_action)

        self.addToolBar(toolbar)

    def _create_menu(self):
        """Creates the menu bar."""
        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        open_action = QAction(QIcon("assets/icons/open.png"), "Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon("assets/icons/save.png"), "Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction(QIcon("assets/icons/exit.png"), "Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        """Opens a file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                content = f.read()
                self._add_tab(file_name, content)

    def save_file(self):
        """Saves the current file."""
        current_widget = self.tabs.currentWidget()
        if current_widget:
            editor = current_widget.layout().itemAt(0).widget()
            with open(self.tabs.tabText(self.tabs.currentIndex()), 'w') as f:
                f.write(editor.toPlainText())

    def _add_tab(self, title, content):
        """Adds a new tab."""
        editor = CodeEditor()
        editor.setPlainText(content)

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(editor)
        container.setLayout(layout)

        self.tabs.addTab(container, title)
        self.tabs.setCurrentWidget(container)

    def close_tab(self, index):
        """Closes a tab."""
        self.tabs.removeTab(index)

def run_editor():
    """Runs the editor."""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
