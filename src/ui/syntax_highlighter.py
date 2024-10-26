from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegularExpression

class MultiLanguageHighlighter(QSyntaxHighlighter):
    """Syntax Highlighter for multiple programming languages."""
    def __init__(self, document, language="python"):
        super().__init__(document)
        self.language = language
        self.setup_rules()

    def setup_rules(self):
        """Define syntax rules for the selected language."""
        self.rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QFont.Bold)

        # Define keywords based on language
        if self.language == "python":
            keywords = ["def", "class", "if", "else", "return", "for", "while", "import"]
        elif self.language == "javascript":
            keywords = ["function", "const", "let", "var", "if", "else", "return", "import", "export"]
        else:  # Markdown
            keywords = ["# ", "## ", "### ", "```", "*", "**"]

        # Compile regular expressions for keywords
        self.rules = [(QRegularExpression(rf'\b{kw}\b'), keyword_format) for kw in keywords]

    def highlightBlock(self, text):
        """Apply highlighting rules to the given block of text."""
        for pattern, fmt in self.rules:
            match = pattern.globalMatch(text)
            while match.hasNext():
                m = match.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)
