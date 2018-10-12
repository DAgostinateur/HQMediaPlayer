from PyQt5.QtWidgets import QSpinBox


# noinspection PyArgumentList
class MillisecondSpinBox(QSpinBox):
    def __init__(self, parent=None):
        super(MillisecondSpinBox, self).__init__(parent)

        self.setGeometry(70, 30, 57, 21)
        self.setMaximum(9999)
        self.setDisplayIntegerBase(10)

        self.valueChanged.connect(self.msb_value_change)

    @property
    def option_scrolling_text(self):
        return self.parentWidget()

    def msb_value_change(self):
        """Spin Millisecond value changed"""
        self.option_scrolling_text.behaviour_tab.options_dialog.behaviour_scrolling_text_speed = self.value()
