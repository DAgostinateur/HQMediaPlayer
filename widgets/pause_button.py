from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtMultimedia import QMediaPlayer

import files
import util


# noinspection PyUnresolvedReferences
class PauseButton(QPushButton):
    def __init__(self, parent=None):
        super(PauseButton, self).__init__(parent)
        self.setGeometry(252, 90, 25, 25)
        self.setToolTip("Pause")
        self.setIcon(QIcon(files.Images.PAUSE))
        self.setIconSize(QSize(25, 25))
        self.setFocusPolicy(Qt.ClickFocus)

        self.released.connect(self.pb_released)
        self.clicked.connect(self.pb_clicked)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    def pb_released(self):
        self.clearFocus()

    def pb_clicked(self):
        if not self.mainwindow.player.state() == QMediaPlayer.StoppedState:
            self.mainwindow.player.pause()

            self.mainwindow.play_button.setToolTip("Play")
            self.mainwindow.play_button.setIcon(QIcon(files.Images.PLAY))
            self.setToolTip("Paused")
            self.setIcon(QIcon(files.Images.PAUSED))
