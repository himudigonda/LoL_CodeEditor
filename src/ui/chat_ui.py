# src/ui/chat_ui.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt

class ChatUI(QWidget):
    """Chat interface for interacting with the code editor."""
    def __init__(self):
        super().__init__()

        # Create chat components
        self.chat_browser = QTextBrowser()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your message...")

        send_button = QPushButton("Send")
        send_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        send_button.clicked.connect(self.send_message)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.chat_browser)
        layout.addWidget(self.chat_input)
        layout.addWidget(send_button, alignment=Qt.AlignRight)
        self.setLayout(layout)

        self.setMaximumWidth(300)  # Limit chat pane width to 300px

    def send_message(self):
        """Display the message in the chat."""
        message = self.chat_input.text()
        if message:
            self.chat_browser.append(f"<b>You:</b> {message}")
            self.chat_input.clear()
