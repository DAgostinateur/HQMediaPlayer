from PyQt5.QtWidgets import QComboBox


# noinspection PyArgumentList
class SelectedDeviceComboBox(QComboBox):
    def __init__(self, parent):
        super(SelectedDeviceComboBox, self).__init__(parent)

        self.setGeometry(10, 40, 311, 21)

        self.currentIndexChanged.connect(self.sdcb_current_index_changed)

    @property
    def option_output_device_box(self):
        return self.parentWidget()

    def sdcb_current_index_changed(self, index):
        self.option_output_device_box.audio_tab.options_dialog.audio_output_device = self.itemText(index)
