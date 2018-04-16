from PyQt5.QtWidgets import QWidget, QDialogButtonBox, QDialog, QTabWidget, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

import files
import util


# noinspection PyUnresolvedReferences,PyArgumentList
class OptionsDialog(QDialog):
    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)
        self.setGeometry(50, 50, 400, 300)
        self.setMinimumSize(400, 300)
        self.setFont(QFont("Consolas", 10))
        self.setWindowTitle("Options")
        self.setWindowIcon(QIcon(files.Images.HQPLAYER_LOGO))
        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))

        self.create_tabs()

        self.button_box = QDialogButtonBox(self)
        self.button_box.setGeometry(20, 250, 360, 32)
        self.button_box.setStandardButtons(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        self.button_box.accepted.connect(self.button_box_accepted)
        self.button_box.rejected.connect(self.button_box_rejected)

    def create_tabs(self):
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(20, 10, 360, 200)
        self.tab_widget.resize(360, 200)

        tab1 = QWidget()

        self.tab_widget.addTab(tab1, "Woh 1")
        button = QPushButton

    def button_box_accepted(self):
        self.close()

    def button_box_rejected(self):
        self.close()
