from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

import files
import util


# noinspection PyUnresolvedReferences
class VolumeSlider(QSlider):
    default_volume = 25
    volume_when_muted = default_volume

    def __init__(self, parent=None):
        super(VolumeSlider, self).__init__(parent)

        self.setGeometry(180, 61, 100, 22)
        self.setToolTip(str(self.default_volume))
        self.setMaximum(100)
        self.setValue(self.default_volume)
        self.setOrientation(Qt.Horizontal)
        self.setFocusPolicy(Qt.ClickFocus)

        self.sliderReleased.connect(self.vs_slider_released)
        self.valueChanged.connect(self.vs_value_changed)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    def vs_slider_released(self):
        self.clearFocus()

    def vs_value_changed(self, value):
        self.mainwindow.player.setVolume(value)
        if self.mainwindow.mute_button.muted:
            self.mainwindow.mute_button.muted = False

        self.mainwindow.mute_button.setIcon(self.get_volume_icon())
        self.setToolTip(str(value))

    def set_volume_when_muted(self):
        self.volume_when_muted = self.value()

    def before_mute_volume(self):
        self.setValue(self.volume_when_muted)

    def mute_volume(self):
        self.setValue(0)

    def increase_volume(self, nb: int):
        self.setValue(self.value() + nb)

    def decrease_volume(self, nb: int):
        self.setValue(self.value() - nb)

    def get_volume_icon(self):
        """Checks the volume and returns the appropriate image for mute_button.

        :return: QIcon with appropriate image
        """
        if self.value() < 1:
            return QIcon(files.Images.VOLUME_0)
        elif self.value() <= 33:
            return QIcon(files.Images.VOLUME_LESS_33)
        elif self.value() <= 66:
            return QIcon(files.Images.VOLUME_LESS_66)
        elif self.value() <= 100:
            return QIcon(files.Images.VOLUME_LESS_100)
        else:
            return QIcon(files.Images.VOLUME_ERROR)
