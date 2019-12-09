from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSlider, QLineEdit
from PyQt5.QtCore import Qt

import files
import util


# noinspection PyUnresolvedReferences
class VolumeSlider(QSlider):
    volume_at_start = None
    volume_when_muted = volume_at_start

    pixel_range = 9

    def __init__(self, parent=None):
        super(VolumeSlider, self).__init__(parent)

        self.volume_at_start = self.mainwindow.options.get_default_volume()

        self.setGeometry(180, 61, 100, 22)
        self.setToolTip(str(self.volume_at_start))
        self.setMaximum(100)
        self.setValue(self.volume_at_start)
        self.setOrientation(Qt.Horizontal)
        self.setFocusPolicy(Qt.ClickFocus)

        self.sliderReleased.connect(self.vs_slider_released)
        self.valueChanged.connect(self.vs_value_changed)

        self.volume_line_edit = QLineEdit(self.music_control_box)
        # 169 is 0 in terms of volume.
        self.volume_line_edit.setGeometry(169, 38, 32, 20)
        self.volume_line_edit.setMouseTracking(False)
        self.volume_line_edit.setInputMask("000")
        self.volume_line_edit.setText(str(self.volume_at_start))
        self.volume_line_edit.setMaxLength(3)
        self.volume_line_edit.setAlignment(Qt.AlignCenter)
        self.volume_line_edit.close()

        self.volume_line_edit.editingFinished.connect(self.vle_editing_finished)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_control_box(self):
        return self.parentWidget()

    def vle_editing_finished(self):
        try:
            if 0 <= int(self.volume_line_edit.text()) <= 100:
                self.setValue(int(self.volume_line_edit.text()))
            else:
                self.volume_line_edit.setText(str(self.value()))
        except ValueError:
            self.volume_line_edit.setText(str(self.value()))

        self.volume_line_edit.clearFocus()
        self.volume_line_edit.close()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.volume_line_edit.move(169 + self.value() - self.get_offset_correction(), 38)
            self.volume_line_edit.show()
            self.volume_line_edit.selectAll()
            self.volume_line_edit.setFocus()
        else:
            QSlider.mouseReleaseEvent(self, event)

    def get_offset_correction(self):
        # pixels       - volume
        # left : right
        # 11   : 11    - (-4)0-4
        # 10   : 12    - 5-13
        # 9    : 13    - 14-22
        # 8    : 14    - 23-31
        # 7    : 15    - 32-40
        # 6    : 16    - 41-49
        # 5    : 17    - 50-58
        # 4    : 18    - 59-67
        # 3    : 19    - 68-76
        # 2    : 20    - 77-85
        # 1    : 21    - 86-94
        # 0    : 22    - 95-100

        for x in range(12):
            big_number = x * self.pixel_range + 4
            if big_number - self.pixel_range + 1 <= self.value() <= big_number:
                return x

    def vs_slider_released(self):
        self.clearFocus()

    def vs_value_changed(self, value):
        self.music_control_box.player.setVolume(value)
        if self.music_control_box.mute_button.muted:
            self.music_control_box.mute_button.muted = False

        self.volume_line_edit.setText(str(self.value()))
        self.music_control_box.mute_button.setIcon(self.get_volume_icon())
        self.setToolTip(str(value))

    def set_volume_when_muted(self):
        self.volume_when_muted = self.value()

    def before_mute_volume(self):
        self.setValue(self.volume_when_muted)

    def mute_volume(self):
        self.setValue(0)

    def increase_volume(self, nb: int = 5):
        self.setValue(self.value() + nb)

    def decrease_volume(self, nb: int = 5):
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
