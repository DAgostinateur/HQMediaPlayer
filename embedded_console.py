from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QTextEdit


class EmbeddedConsole(QTextEdit):
    CONSOLE_STYLESHEET = ("QTextEdit {border-style: solid; border-width: 3px;"
                          "background-color: #000; border-color: #FFF;"
                          "color: #C8C8C8; font-size: 13px}")

    def __init__(self, parent=None):
        super(EmbeddedConsole, self).__init__(parent)
        self.setGeometry(9, 34, 350, 231)
        self.setReadOnly(True)
        self.setStyleSheet(self.CONSOLE_STYLESHEET)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def write(self, msg):
        """Add msg to the console's output, on a new line."""
        self.insertPlainText(msg + '\n')
        self.moveCursor(QTextCursor.End)
