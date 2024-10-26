from PyQt5.QtWidgets import (
    QMainWindow, QSplitter, QTabWidget, QStatusBar, QToolBar, QAction,
    QFileDialog, QMessageBox, QVBoxLayout, QWidget, QStyleFactory, QDialog,
    QLabel, QTextBrowser, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon
from src.ui.editor import CodeEditor
from src.ui.chat_ui import ChatUI
from src.ui.file_explorer import FileExplorer
from src.ui.plugin_manager import PluginManager
from src.ui.terminal import TerminalWidget

class SearchReplaceDialog(QDialog):
    """Advanced Search & Replace Dialog."""
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.setWindowTitle("Search & Replace")
        layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search...")
        layout.addWidget(self.search_input)

        self.replace_input = QLineEdit(self)
        self.replace_input.setPlaceholderText("Replace with...")
        layout.addWidget(self.replace_input)

        replace_button = QPushButton("Replace All", self)
        replace_button.clicked.connect(self.replace_all)
        layout.addWidget(replace_button)

        self.setLayout(layout)

    def replace_all(self):
        """Replace all occurrences of the search text."""
        search_text = self.search_input.text()
        replace_text = self.replace_input.text()
        content = self.editor.toPlainText()
        updated_content = content.replace(search_text, replace_text)
        self.editor.setPlainText(updated_content)

class MainWindow(QMainWindow):
    """Main window for LoL_CodeEditor."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LoL_CodeEditor - AI-powered Code Editor")
        self.setGeometry(100, 100, 1400, 900)

        self.initialize_ui()
        self.start_autosave()

    def initialize_ui(self):
        """Initialize UI components."""
        # Left Panel: File Explorer + Plugins
        self.left_panel = QTabWidget()
        self.file_explorer = FileExplorer(self._open_file_in_tab)
        self.plugin_manager = PluginManager()
        self.left_panel.addTab(self.file_explorer, "Explorer")
        self.left_panel.addTab(self.plugin_manager, "Plugins")

        # Center: Tabbed Editor
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.confirm_tab_close)

        # Right Panel: Chat UI
        self.chat_widget = ChatUI()
        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.addWidget(self.chat_widget)

        # Horizontal Splitter
        self.horizontal_splitter = QSplitter(Qt.Horizontal)
        self.horizontal_splitter.addWidget(self.left_panel)
        self.horizontal_splitter.addWidget(self.tabs)
        self.horizontal_splitter.addWidget(chat_container)
        self.horizontal_splitter.setSizes([300, 800, 300])

        # Terminal at the Bottom
        self.terminal = TerminalWidget()
        self.vertical_splitter = QSplitter(Qt.Vertical)
        self.vertical_splitter.addWidget(self.horizontal_splitter)
        self.vertical_splitter.addWidget(self.terminal)
        self.vertical_splitter.setSizes([700, 200])

        self.setCentralWidget(self.vertical_splitter)
        self._create_toolbar()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.setStyle(QStyleFactory.create("Fusion"))

    def _open_file_in_tab(self, file_path, content):
        """Add a new tab with the opened file content."""
        editor = CodeEditor()
        editor.setPlainText(content)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(editor)

        self.tabs.addTab(container, file_path)
        self.tabs.setCurrentWidget(container)
        self.status_bar.showMessage(f"Opened: {file_path}")

    def _create_toolbar(self):
        """Create toolbar."""
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

        # Markdown Preview Action
        preview_action = QAction("Markdown Preview", self)
        preview_action.triggered.connect(self.open_markdown_preview)
        toolbar.addAction(preview_action)

        # Search & Replace Action
        search_replace_action = QAction("Search & Replace", self)
        search_replace_action.triggered.connect(self.open_search_replace)
        toolbar.addAction(search_replace_action)

        self.addToolBar(toolbar)

    def new_file(self):
        """Create a new file."""
        editor = CodeEditor()
        self.add_tab(editor, "Untitled")

    def open_file_dialog(self):
        """Open file and display in new tab."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_name:
            with open(file_name, 'r') as f:
                content = f.read()
            editor = CodeEditor()
            editor.setPlainText(content)
            self.add_tab(editor, file_name)

    def open_markdown_preview(self):
        """Open Markdown editor with live preview."""
        editor = CodeEditor()
        preview = QTextBrowser()

        def update_preview():
            markdown_text = editor.toPlainText()
            html_content = markdown_text.replace("#", "<h1>").replace("**", "<b>")
            preview.setHtml(html_content)

        editor.textChanged.connect(update_preview)
        self.add_tab(editor, "Markdown Editor")
        self.add_tab(preview, "Markdown Preview")

    def open_search_replace(self):
        """Open Search & Replace dialog."""
        editor = self.get_current_editor()
        if editor:
            dialog = SearchReplaceDialog(editor)
            dialog.exec_()

    def add_tab(self, widget, title):
        """Add a new tab."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(widget)
        self.tabs.addTab(container, title)
        self.tabs.setCurrentWidget(container)

    def confirm_tab_close(self, index):
        """Confirm tab close."""
        reply = QMessageBox.question(self, "Close Tab", "Do you want to close this tab?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.tabs.removeTab(index)

    def get_current_editor(self):
        """Get the current editor."""
        container = self.tabs.currentWidget()
        if container:
            return container.layout().itemAt(0).widget()
        return None

    def start_autosave(self):
        """Start autosave."""
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autosave_tabs)
        self.autosave_timer.start(30000)

    def autosave_tabs(self):
        """Autosave open tabs."""
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            editor = widget.layout().itemAt(0).widget()
            file_path = self.tabs.tabText(i)
            if file_path != "Untitled":
                with open(file_path, "w") as f:
                    f.write(editor.toPlainText())
                self.status_bar.showMessage(f"Autosaved: {file_path}")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
