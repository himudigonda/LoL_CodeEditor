# src/ui/editor.py

from PyQt5.QtWidgets import QPlainTextEdit, QWidget
from PyQt5.QtGui import QFont, QPainter, QColor
from PyQt5.QtCore import Qt, QRect

class LineNumberArea(QWidget):
    """Line number area synchronized with the code editor."""
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setFixedWidth(50)

    def paintEvent(self, event):
        """Paint the line numbers using QPainter."""
        painter = QPainter(self)  # Properly initialize QPainter
        painter.fillRect(event.rect(), QColor(240, 240, 240))  # Light gray background

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        # Draw each visible block number
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(
                    0, int(top), self.width(), self.editor.fontMetrics().height(),
                    Qt.AlignRight, number
                )
            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1

    def update_width(self, block_count):
        """Adjust the width based on the number of lines."""
        width = max(30, self.fontMetrics().width(str(block_count)) + 10)
        self.setFixedWidth(width)

    def update(self, *args):
        """Repaint and resize the widget."""
        self.update_width(self.editor.blockCount())
        super().update(*args)


class CodeEditor(QPlainTextEdit):
    """Custom code editor with a synchronized line number area."""
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)

        # Use a monospaced font for consistent spacing
        font = QFont("Courier New", 12)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

        # Connect signals to synchronize the editor and line numbers
        self.blockCountChanged.connect(self.line_number_area.update_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.verticalScrollBar().valueChanged.connect(self.line_number_area.update)

    def resizeEvent(self, event):
        """Resize the line number area along with the editor."""
        super().resizeEvent(event)
        rect = self.contentsRect()
        self.line_number_area.setGeometry(QRect(rect.left(), rect.top(), 50, rect.height()))

    def update_line_number_area(self, rect, dy):
        """Update the line number area on editor changes."""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.line_number_area.update_width(self.blockCount())
