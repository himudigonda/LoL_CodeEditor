from PyQt5.QtWidgets import QPlainTextEdit, QWidget
from PyQt5.QtGui import QFont, QPainter, QColor
from PyQt5.QtCore import QRect, QSize, Qt
from src.ui.syntax_highlighter import MultiLanguageHighlighter  # Correct import

class LineNumberArea(QWidget):
    """Line number area for the code editor."""
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
                                 self.editor.fontMetrics().height(), Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1

class CodeEditor(QPlainTextEdit):
    """Custom code editor with syntax highlighting and line numbers."""
    def __init__(self, language="python"):
        super().__init__()
        self.line_number_area = LineNumberArea(self)

        # Set font for the editor
        font = QFont("Fira Code", 12)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

        # Initialize syntax highlighter
        self.highlighter = MultiLanguageHighlighter(self.document(), language)

        # Connect signals for line numbers
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.verticalScrollBar().valueChanged.connect(self.line_number_area.update)

    def line_number_area_width(self):
        """Calculate the width of the line number area."""
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def resizeEvent(self, event):
        """Handle resize events."""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(),
                                                self.line_number_area_width(), cr.height()))

    def update_line_number_area(self, rect, dy):
        """Update the line number area during scrolling."""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

    def update_line_number_area_width(self):
        """Adjust the margin for the line number area."""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
