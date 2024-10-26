from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ["def", "class", "if", "else", "return", "for", "while", "import"]

        self.rules = [(QRegularExpression(rf'\b{keyword}\b'), keyword_format) for keyword in keywords]

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("magenta"))
        self.rules.append((QRegularExpression(r'"[^"]*"'), string_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            match = pattern.globalMatch(text)
            while match.hasNext():
                m = match.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)
