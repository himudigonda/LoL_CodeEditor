from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit
from PyQt5.QtCore import Qt, QProcess, QTimer

class TerminalWidget(QWidget):
    """A terminal widget to run shell commands."""
    def __init__(self):
        super().__init__()

        self.process = QProcess(self)

        # Create output and input areas
        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        self.output_area.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.input_area = QLineEdit()
        self.input_area.setPlaceholderText("Enter command...")
        self.input_area.returnPressed.connect(self.run_command)

        layout = QVBoxLayout(self)
        layout.addWidget(self.output_area)
        layout.addWidget(self.input_area)

        # Focus on input when the terminal opens
        QTimer.singleShot(0, self.input_area.setFocus)

    def run_command(self):
        """Execute a shell command."""
        command = self.input_area.text().strip()
        if command:
            self.output_area.appendPlainText(f"$ {command}")
            self.process.start(command)
            self.process.readyReadStandardOutput.connect(self.display_output)
            self.process.readyReadStandardError.connect(self.display_error)
            self.input_area.clear()

    def display_output(self):
        """Show standard output."""
        output = self.process.readAllStandardOutput().data().decode().strip()
        self.output_area.appendPlainText(output)

    def display_error(self):
        """Show error output."""
        error = self.process.readAllStandardError().data().decode().strip()
        self.output_area.appendPlainText(f"Error: {error}")
