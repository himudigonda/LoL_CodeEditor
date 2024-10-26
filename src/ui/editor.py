from PyQt5.QtWidgets import QPlainTextEdit, QWidget
from PyQt5.QtGui import QFont, QPainter, QColor
from PyQt5.QtCore import QRect, QSize, Qt
from src.ui.syntax_highlighter import PythonHighlighter

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor(240, 240, 240))

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, int(top), self.width() - 5,
                                 self.editor.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)

        font = QFont("Fira Code", 12)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

        self.highlighter = PythonHighlighter(self.document())

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.verticalScrollBar().valueChanged.connect(self.line_number_area.update)
    def lint_code(self):
        """Run flake8 to lint the code."""
        try:
            text = self.toPlainText()
            result = subprocess.run(
                ["flake8", "--stdin-display-name", "current_file.py", "-"],
                input=text.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output = result.stdout.decode().strip()
            if output:
                self.parent().status_bar.showMessage(f"Lint Issues: {output.splitlines()[0]}")
            else:
                self.parent().status_bar.showMessage("No Lint Issues Found!")
        except FileNotFoundError:
            QMessageBox.critical(self, "Flake8 Not Found", "Please install 'flake8' to use this feature.")

    def format_code(self):
        """Format the current code using 'black'."""
        try:
            text = self.toPlainText()
            result = subprocess.run(
                ["black", "-q", "-"],
                input=text.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode == 0:
                formatted_code = result.stdout.decode()
                self.setPlainText(formatted_code)
                QMessageBox.information(self, "Format", "Code formatted successfully!")
            else:
                error = result.stderr.decode()
                QMessageBox.warning(self, "Format Error", f"Error: {error}")
        except FileNotFoundError:
            QMessageBox.critical(self, "Black Not Found", "Please install 'black' to use this feature.")

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(),
                                                self.line_number_area_width(), cr.height()))

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
