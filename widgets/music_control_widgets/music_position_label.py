from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

import util


# noinspection PyUnresolvedReferences
class MusicPositionLabel(QLabel):
    def __init__(self, parent=None):
        super(MusicPositionLabel, self).__init__(parent)
        self.setGeometry(10, 50, 63, 15)
        self.setText("00:00")
        self.setAlignment(Qt.AlignRight)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_control_box(self):
        return self.parentWidget()

    def reset_time(self):
        self.setText("00:00")
