from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtCore import Qt

from widgets.option_dialog_widgets.behaviour_tab_section import nothing_radio_button, restart_radio_button


# noinspection PyArgumentList
class OptionPlayButtonBox(QGroupBox):
    def __init__(self, parent=None):
        super(OptionPlayButtonBox, self).__init__(parent)

        self.setGeometry(10, 10, 131, 71)
        self.setToolTip("When a song is playing, the play button (when clicked) will...")
        self.setTitle("Play Button")
        self.setAlignment(Qt.AlignCenter)

        self.radio_nothing = nothing_radio_button.NothingRadioButton(self)
        self.radio_restart = restart_radio_button.RestartRadioButton(self)

    @property
    def behaviour_tab(self):
        return self.parentWidget()
