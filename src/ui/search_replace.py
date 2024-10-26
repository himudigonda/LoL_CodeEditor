# src/ui/search_replace.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import Qt

class SearchReplaceWidget(QWidget):
    """Search & Replace widget for global and inline search."""
    def __init__(self, editor, status_bar):
        super().__init__()
        self.editor = editor
        self.status_bar = status_bar

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self.search_text)

        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replace with...")

        replace_button = QPushButton("Replace All")
        replace_button.clicked.connect(self.replace_all)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Search & Replace"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.replace_input)
        layout.addWidget(replace_button)
        self.setLayout(layout)

    def search_text(self):
        """Highlight all occurrences of the search text."""
        search_term = self.search_input.text()
        if self.editor and search_term:
            cursor = self.editor.textCursor()
            document = self.editor.document()

            cursor.beginEditBlock()
            cursor.movePosition(cursor.Start)
            while not cursor.isNull() and not cursor.atEnd():
                cursor = document.find(search_term, cursor)
                if cursor.hasSelection():
                    self.editor.setTextCursor(cursor)
            cursor.endEditBlock()

    def replace_all(self):
        """Replace all occurrences of the search text with the replacement text."""
        search_term = self.search_input.text()
        replace_term = self.replace_input.text()

        if search_term and replace_term:
            text = self.editor.toPlainText()
            updated_text = text.replace(search_term, replace_term)
            self.editor.setPlainText(updated_text)
            self.status_bar.showMessage(f"Replaced all occurrences of '{search_term}' with '{replace_term}'")
