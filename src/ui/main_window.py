from PyQt5.QtWidgets import (
    QMainWindow, QSplitter, QTabWidget, QToolBar, QAction, QStatusBar,
    QVBoxLayout, QWidget, QFileDialog, QMessageBox, QStyleFactory
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from src.ui.editor import CodeEditor
from src.ui.chat_ui import ChatUI
from src.ui.file_explorer import FileExplorer
from src.ui.plugin_manager import PluginManager
from src.ui.terminal import TerminalWidget

class MainWindow(QMainWindow):
    """Main window for the LightCode editor."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LightCode - AI-powered Code Editor")
        self.setGeometry(100, 100, 1400, 800)

        self.splitter = QSplitter(Qt.Horizontal)

        # Left Panel: File Explorer + Plugin Manager
        self.left_panel = QTabWidget()
        self.file_explorer = FileExplorer(self._open_file_in_tab)
        self.plugin_manager = PluginManager()
        self.left_panel.addTab(self.file_explorer, "Explorer")
        self.left_panel.addTab(self.plugin_manager, "Plugins")
        self.splitter.addWidget(self.left_panel)

        # Center: Tabbed Editor
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.confirm_tab_close)
        self.splitter.addWidget(self.tabs)

        # Right Panel: Chat UI + Terminal
        self.right_panel = QTabWidget()
        self.chat_widget = ChatUI()
        self.terminal = TerminalWidget()
        self.right_panel.addTab(self.chat_widget, "Chat")
        self.right_panel.addTab(self.terminal, "Terminal")
        self.splitter.addWidget(self.right_panel)

        # Set splitter proportions
        self.splitter.setSizes([300, 900, 300])

        self.setCentralWidget(self.splitter)
        self._create_toolbar()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.setStyle(QStyleFactory.create("Fusion"))

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setIconSize(QSize(24, 24))

        open_action = QAction(QIcon("assets/open.png"), "Open", self)
        open_action.triggered.connect(self.open_file_dialog)
        toolbar.addAction(open_action)

        self.addToolBar(toolbar)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_name:
            with open(file_name, 'r') as f:
                content = f.read()
            self._open_file_in_tab(file_name, content)

    def _open_file_in_tab(self, file_path, content):
        editor = CodeEditor()
        editor.setPlainText(content)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(editor)

        self.tabs.addTab(container, file_path)
        self.tabs.setCurrentWidget(container)
        self.status_bar.showMessage(f"Opened: {file_path}")

    def confirm_tab_close(self, index):
        reply = QMessageBox.question(self, "Close Tab", "Do you want to close this tab?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.tabs.removeTab(index)
