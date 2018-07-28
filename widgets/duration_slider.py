from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider

import util
import files


# noinspection PyUnresolvedReferences
class DurationSlider(QSlider):
    def __init__(self, parent=None):
        super(DurationSlider, self).__init__(parent)
        self.setDisabled(True)
        self.setGeometry(10, 20, 271, 22)
        self.setToolTip("Seek")
        self.setStyleSheet(self.slider_stylesheet)

        self.setMaximum(271)
        self.setOrientation(Qt.Horizontal)
        self.setFocusPolicy(Qt.ClickFocus)

        self.sliderMoved.connect(self.ds_slider_moved)
        self.sliderPressed.connect(self.ds_slider_pressed)
        self.sliderReleased.connect(self.ds_slider_released)

    @property
    def slider_stylesheet(self):
        stylesheet = ""
        with open(files.DURATION_SLIDER_STYLESHEET, 'r') as f:
            for line in f:
                stylesheet += line.strip('\n')
        return stylesheet

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_control_box(self):
        return self.parentWidget()

    def ds_slider_moved(self, value):
        self.music_control_box.player.setPosition(value)

    def ds_slider_pressed(self):
        self.music_control_box.player.setMuted(True)

    def ds_slider_released(self):
        self.music_control_box.player.setMuted(False)
        self.clearFocus()

    def reset_slider(self):
        self.setValue(0)
        self.setMaximum(271)
