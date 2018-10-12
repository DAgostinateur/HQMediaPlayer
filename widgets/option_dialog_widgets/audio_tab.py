from PyQt5.QtWidgets import QWidget

import util
from widgets.option_dialog_widgets.audio_tab_section import option_output_device_box


# noinspection PyArgumentList
class AudioTab(QWidget):
    def __init__(self, parent=None):
        super(AudioTab, self).__init__(parent)

        self.option_output_device = option_output_device_box.OptionOutputDeviceBox(self)

    @property
    def options_dialog(self):
        return util.get_upper_parentwidget(self, 3)
