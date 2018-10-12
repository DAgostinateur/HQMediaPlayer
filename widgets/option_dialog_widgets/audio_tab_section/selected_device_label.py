from PyQt5.QtWidgets import QLabel


# noinspection PyArgumentList
class SelectedDeviceLabel(QLabel):
    def __init__(self, parent):
        super(SelectedDeviceLabel, self).__init__(parent)

        self.setGeometry(10, 17, 311, 16)
        self.setToolTip("N/A")
        self.setText("Current: N/A")
