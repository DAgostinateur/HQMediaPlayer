from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize

import files
import util


# noinspection PyUnresolvedReferences
class StopButton(QPushButton):
    def __init__(self, parent=None):
        super(StopButton, self).__init__(parent)

        self.setGeometry(252, 125, 25, 25)
        self.setToolTip("Stopped")
        self.setIcon(QIcon(files.Images.STOPPED))
        self.setIconSize(QSize(25, 25))
        self.setFocusPolicy(Qt.ClickFocus)

        self.released.connect(self.sb_released)
        self.clicked.connect(self.sb_clicked)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    def sb_released(self):
        self.clearFocus()

    def sb_clicked(self):
        self.mainwindow.player.stop()
        self.mainwindow.reset_duration_slider()
        self.mainwindow.reset_music_info()
        self.mainwindow.duration_slider.setDisabled(True)

        self.mainwindow.pause_button.setToolTip("Pause")
        self.mainwindow.pause_button.setIcon(QIcon(files.Images.PAUSE))
        self.mainwindow.play_button.setToolTip("Play")
        self.mainwindow.play_button.setIcon(QIcon(files.Images.PLAY))
        self.setToolTip("Stopped")
        self.setIcon(QIcon(files.Images.STOPPED))
