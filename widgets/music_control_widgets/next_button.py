from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize

import files
import util


# noinspection PyUnresolvedReferences
class NextButton(QPushButton):
    def __init__(self, parent=None):
        super(NextButton, self).__init__(parent)
        self.setGeometry(252, 90, 25, 25)
        self.setToolTip("Next")
        self.setIcon(QIcon(files.Images.NEXT))
        self.setIconSize(QSize(25, 25))
        self.setFocusPolicy(Qt.ClickFocus)

        self.released.connect(self.nb_released)
        self.clicked.connect(self.nb_clicked)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_control_box(self):
        return self.parentWidget()

    def nb_released(self):
        self.clearFocus()

    def nb_clicked(self):
        if self.music_control_box.player.has_playlist:
            self.music_control_box.player.next_index()
