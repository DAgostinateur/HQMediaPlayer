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

    @property
    def music_control_box(self):
        return self.parentWidget()

    def sb_released(self):
        self.clearFocus()

    def sb_clicked(self):
        self.mainwindow.player.stop()
        self.music_control_box.reset_duration()
        self.music_control_box.duration_slider.setDisabled(True)
        # self.mainwindow.music_info_box.reset_music_info()

        self.music_control_box.set_stopped_state_buttons()
        self.setToolTip("Stopped")
        self.setIcon(QIcon(files.Images.STOPPED))
