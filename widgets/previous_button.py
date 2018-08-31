from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize

import files
import util


# noinspection PyUnresolvedReferences
class PreviousButton(QPushButton):
    def __init__(self, parent=None):
        super(PreviousButton, self).__init__(parent)
        self.setGeometry(180, 90, 25, 25)
        self.setToolTip("Previous")
        self.setIcon(QIcon(files.Images.PREVIOUS))
        self.setIconSize(QSize(25, 25))
        self.setFocusPolicy(Qt.ClickFocus)

        self.released.connect(self.prb_released)
        self.clicked.connect(self.prb_clicked)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_control_box(self):
        return self.parentWidget()

    def prb_released(self):
        self.clearFocus()

    def prb_clicked(self):
        if self.music_control_box.player.has_playlist:
            self.music_control_box.player.previous_index()
