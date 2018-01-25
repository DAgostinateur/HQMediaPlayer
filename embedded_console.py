from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QTextEdit
import files


class EmbeddedConsole(QTextEdit):
    CONSOLE_STYLESHEET = ("QTextEdit {border-style: solid; border-width: 3px;"
                          "background-color: #000; border-color: #DDD;"
                          "color: #C8C8C8; font-size: 13px}")

    def __init__(self, parent=None):
        super(EmbeddedConsole, self).__init__(parent)
        self.setGeometry(9, 59, 350, 231)
        self.setReadOnly(True)
        self.setStyleSheet(self.CONSOLE_STYLESHEET)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def write(self, msg):
        """Add msg to the console's output, on a new line.
           Also writes it to a file"""
        with open(files.DEBUG_FILE, 'a') as f:
            f.write(msg + '\n')

        self.insertPlainText(msg + '\n')
        self.moveCursor(QTextCursor.End)
