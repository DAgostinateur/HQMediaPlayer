from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize

import files
import util


# noinspection PyUnresolvedReferences
class RepeatButton(QPushButton):
    def __init__(self, parent=None):
        super(RepeatButton, self).__init__(parent)

        self.repeating = False

        self.setGeometry(216, 125, 25, 25)
        self.setToolTip("Repeat")
        self.setIcon(QIcon(files.Images.REPEAT))
        self.setIconSize(QSize(25, 25))
        self.setFocusPolicy(Qt.ClickFocus)

        self.released.connect(self.rb_released)
        self.clicked.connect(self.rb_clicked)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_control_box(self):
        return self.parentWidget()

    def rb_released(self):
        self.clearFocus()

    def rb_clicked(self):
        if self.repeating:
            self.setToolTip("Repeat")
            self.setIcon(QIcon(files.Images.REPEAT))
        else:
            self.setToolTip("Repeating")
            self.setIcon(QIcon(files.Images.REPEATING))

        self.repeating = not self.repeating
