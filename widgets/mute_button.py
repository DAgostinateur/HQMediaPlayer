from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize

import files
import util


# noinspection PyUnresolvedReferences
class MuteButton(QPushButton):
    def __init__(self, parent=None):
        super(MuteButton, self).__init__(parent)

        self.muted = False

        self.setGeometry(180, 90, 25, 25)
        self.setToolTip("Mute")
        self.setIcon(QIcon(files.Images.VOLUME_LESS_33))
        self.setIconSize(QSize(25, 25))
        self.setFocusPolicy(Qt.ClickFocus)

        self.released.connect(self.mb_released)
        self.clicked.connect(self.mb_clicked)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    def mb_released(self):
        self.clearFocus()

    def mb_clicked(self):
        if self.muted:
            self.setToolTip("Muted")
            self.setIcon(self.mainwindow.volume_slider.get_volume_icon())
            self.mainwindow.volume_slider.before_mute_volume()
        else:
            self.mainwindow.volume_slider.set_volume_when_muted()
            self.mainwindow.volume_slider.mute_volume()
            self.setToolTip("Mute")
            self.setIcon(QIcon(files.Images.MUTED))

        self.muted = not self.muted
