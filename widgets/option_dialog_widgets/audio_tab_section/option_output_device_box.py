from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtCore import Qt

from widgets.option_dialog_widgets.audio_tab_section import selected_device_label, selected_device_combobox


# noinspection PyArgumentList
class OptionOutputDeviceBox(QGroupBox):
    def __init__(self, parent=None):
        super(OptionOutputDeviceBox, self).__init__(parent)

        self.setGeometry(10, 10, 331, 71)
        # self.setToolTip("")
        self.setTitle("Audio Output Device (Doesn't work)")
        self.setAlignment(Qt.AlignCenter)

        self.label_selected_device = selected_device_label.SelectedDeviceLabel(self)
        self.combo_box_selected_device = selected_device_combobox.SelectedDeviceComboBox(self)

    @property
    def audio_tab(self):
        return self.parentWidget()
