from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt

class ChatUI(QWidget):
    """Chat interface for interacting with the code editor."""
    def __init__(self):
        super().__init__()

        self.chat_browser = QTextBrowser()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your message...")

        send_button = QPushButton("Send")
        send_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        send_button.clicked.connect(self.send_message)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_browser)
        layout.addWidget(self.chat_input)
        layout.addWidget(send_button, alignment=Qt.AlignRight)
        self.setLayout(layout)

        self.chat_input.returnPressed.connect(self.send_message)  # Send on Enter key press

    def send_message(self):
        """Display the message in the chat."""
        message = self.chat_input.text().strip()
        if message:
            self.chat_browser.append(f"<b>You:</b> {message}")
            self.chat_input.clear()
