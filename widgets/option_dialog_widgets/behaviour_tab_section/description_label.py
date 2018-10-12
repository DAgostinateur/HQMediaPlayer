from PyQt5.QtWidgets import QLabel


# noinspection PyArgumentList
class LabelDescription(QLabel):
    def __init__(self, parent):
        super(LabelDescription, self).__init__(parent)

        self.setGeometry(10, 20, 47, 45)
        self.setToolTip("1000 millisecond = One character per second")
        self.setText("Scroll Speed (ms)")
        self.setWordWrap(True)

    @property
    def option_scrolling_text(self):
        return self.parentWidget()
