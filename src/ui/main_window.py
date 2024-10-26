from PyQt5.QtWidgets import (
    QMainWindow, QSplitter, QTabWidget, QStatusBar, QToolBar,
    QAction, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QStyleFactory
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon
from src.ui.editor import CodeEditor
from src.ui.chat_ui import ChatUI
from src.ui.file_explorer import FileExplorer
from src.ui.plugin_manager import PluginManager
from src.ui.terminal import TerminalWidget
from src.settings_manager import SettingsManager
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel

class ShortcutsViewer(QDialog):
    """A simple dialog to display available shortcuts."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keyboard Shortcuts")
        layout = QVBoxLayout()
        shortcuts = [
            ("Ctrl+N", "New File"),
            ("Ctrl+O", "Open File"),
            ("Ctrl+T", "Toggle Terminal"),
        ]
        for shortcut, desc in shortcuts:
            layout.addWidget(QLabel(f"{shortcut}: {desc}"))
        self.setLayout(layout)

class MainWindow(QMainWindow):
    """Main window for LightCode with VS Code-style layout."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LightCode - AI-powered Code Editor")
        self.setGeometry(100, 100, 1400, 900)

        # Initialize settings and theme
        self.settings_manager = SettingsManager()
        self.current_theme = self.settings_manager.settings.get("theme", "light")
        self.apply_theme(self.current_theme)

        # Initialize all UI elements
        self.initialize_ui()

        # Start autosave timer
        self.start_autosave()

    def initialize_ui(self):
        """Initialize all UI components and layout."""
        # === Left Panel: File Explorer + Plugins ===
        self.left_panel = QTabWidget()
        self.file_explorer = FileExplorer(self._open_file_in_tab)
        self.plugin_manager = PluginManager()
        self.left_panel.addTab(self.file_explorer, "Explorer")
        self.left_panel.addTab(self.plugin_manager, "Plugins")

        # === Center: Tabbed Editor ===
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.confirm_tab_close)

        # === Right Panel: Chat UI ===
        self.chat_widget = ChatUI()
        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.addWidget(self.chat_widget)

        # === Horizontal Split: Left | Center | Right ===
        self.horizontal_splitter = QSplitter(Qt.Horizontal)
        self.horizontal_splitter.addWidget(self.left_panel)
        self.horizontal_splitter.addWidget(self.tabs)
        self.horizontal_splitter.addWidget(chat_container)
        self.horizontal_splitter.setSizes([300, 800, 300])

        # === Terminal at the Bottom ===
        self.terminal = TerminalWidget()
        self.vertical_splitter = QSplitter(Qt.Vertical)
        self.vertical_splitter.addWidget(self.horizontal_splitter)
        self.vertical_splitter.addWidget(self.terminal)
        self.vertical_splitter.setSizes([700, 200])

        # Set the central widget
        self.setCentralWidget(self.vertical_splitter)

        # Create toolbar
        self._create_toolbar()

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Apply Fusion style
        self.setStyle(QStyleFactory.create("Fusion"))

    def _create_toolbar(self):
        """Create the main toolbar."""
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setIconSize(QSize(24, 24))

        # New File Action
        new_file_action = QAction(QIcon("assets/open.png"), "New File", self)
        new_file_action.setShortcut("Ctrl+N")
        new_file_action.triggered.connect(self.new_file)
        toolbar.addAction(new_file_action)

        # Open File Action
        open_action = QAction(QIcon("assets/open.png"), "Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        toolbar.addAction(open_action)

        # Toggle Terminal Action
        toggle_terminal_action = QAction("Toggle Terminal", self)
        toggle_terminal_action.setShortcut("Ctrl+T")
        toggle_terminal_action.triggered.connect(self.toggle_terminal)
        toolbar.addAction(toggle_terminal_action)

        # Show Shortcuts Action
        shortcuts_action = QAction("Shortcuts", self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        toolbar.addAction(shortcuts_action)

        self.addToolBar(toolbar)

    def show_shortcuts(self):
        """Show the shortcuts viewer."""
        viewer = ShortcutsViewer()
        viewer.exec_()

    def new_file(self):
        """Create a new untitled file."""
        editor = CodeEditor()
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(editor)
        self.tabs.addTab(container, "Untitled")
        self.tabs.setCurrentWidget(container)

    def open_file_dialog(self):
        """Open a file and display it in a new tab."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_name:
            with open(file_name, 'r') as f:
                content = f.read()
            self._open_file_in_tab(file_name, content)

    def _open_file_in_tab(self, file_path, content):
        """Add a new tab with the file content."""
        editor = CodeEditor()
        editor.setPlainText(content)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(editor)
        self.tabs.addTab(container, file_path)
        self.tabs.setCurrentWidget(container)
        self.status_bar.showMessage(f"Opened: {file_path}")

    def confirm_tab_close(self, index):
        """Confirm before closing a tab."""
        reply = QMessageBox.question(
            self, "Close Tab", "Do you want to close this tab?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.tabs.removeTab(index)

    def toggle_terminal(self):
        """Toggle the visibility of the terminal."""
        if self.terminal.isVisible():
            self.terminal.hide()
        else:
            self.terminal.show()

    def start_autosave(self):
        """Start the autosave timer."""
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autosave_tabs)
        self.autosave_timer.start(30000)  # Autosave every 30 seconds

    def autosave_tabs(self):
        """Save all open tabs."""
        for index in range(self.tabs.count()):
            widget = self.tabs.widget(index)
            editor = widget.layout().itemAt(0).widget()
            file_path = self.tabs.tabText(index)
            if file_path != "Untitled":
                with open(file_path, "w") as f:
                    f.write(editor.toPlainText())
                self.status_bar.showMessage(f"Autosaved: {file_path}")
    def apply_theme(self, theme):
        """Apply the selected theme."""
        if theme == "dark":
            self.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        else:
            self.setStyleSheet("")
