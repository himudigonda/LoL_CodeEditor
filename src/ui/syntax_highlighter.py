# src/ui/syntax_highlighter.py

from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegularExpression


class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Python code."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rules = []

        # Keyword format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ["def", "class", "if", "else", "while", "for", "return"]
        for keyword in keywords:
            self._rules.append((QRegularExpression(rf'\b{keyword}\b'), keyword_format))

        # String format
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("magenta"))
        self._rules.append((QRegularExpression(r'"[^"]*"'), string_format))

    def highlightBlock(self, text):
        """Apply syntax highlighting."""
        for pattern, format in self._rules:
            match = pattern.globalMatch(text)
            while match.hasNext():
                m = match.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), format)
