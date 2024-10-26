# src/ui/terminal.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit
from PyQt5.QtCore import Qt, QProcess

class TerminalWidget(QWidget):
    """A terminal widget to run shell commands."""
    def __init__(self):
        super().__init__()
        self.process = QProcess(self)

        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)

        self.input_area = QLineEdit()
        self.input_area.setPlaceholderText("Enter command...")
        self.input_area.returnPressed.connect(self.run_command)

        layout = QVBoxLayout()
        layout.addWidget(self.output_area)
        layout.addWidget(self.input_area)
        self.setLayout(layout)

    def run_command(self):
        """Run a shell command and display the output."""
        command = self.input_area.text().strip()
        if command:
            self.process.start(command)
            self.process.readyReadStandardOutput.connect(self.display_output)

    def display_output(self):
        """Display the command output."""
        output = self.process.readAllStandardOutput().data().decode()
        self.output_area.appendPlainText(output)
