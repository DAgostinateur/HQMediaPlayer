from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtCore import Qt

from widgets.option_dialog_widgets.behaviour_tab_section import description_label, millisecond_spinbox


# noinspection PyArgumentList
class OptionScrollingTextBox(QGroupBox):
    def __init__(self, parent=None):
        super(OptionScrollingTextBox, self).__init__(parent)

        self.setGeometry(10, 85, 131, 81)
        self.setTitle("Scrolling Text")
        self.setAlignment(Qt.AlignCenter)

        self.label_description = description_label.LabelDescription(self)
        self.spin_millisecond = millisecond_spinbox.MillisecondSpinBox(self)

    @property
    def behaviour_tab(self):
        return self.parentWidget()
