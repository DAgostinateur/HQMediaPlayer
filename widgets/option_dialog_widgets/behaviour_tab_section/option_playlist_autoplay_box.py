from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtCore import Qt

from widgets.option_dialog_widgets.behaviour_tab_section import autoplay_radio_button, no_autoplay_radio_button


# noinspection PyArgumentList
class OptionPlaylistAutoplayBox(QGroupBox):
    def __init__(self, parent=None):
        super(OptionPlaylistAutoplayBox, self).__init__(parent)

        self.setGeometry(150, 10, 131, 71)
        self.setToolTip("When starting the playlist, it will...")
        self.setTitle("Playlist Autoplay")
        self.setAlignment(Qt.AlignCenter)

        self.radio_autoplay = autoplay_radio_button.AutoplayRadioButton(self)
        self.radio_no_autoplay = no_autoplay_radio_button.NoAutoplayRadioButton(self)

    @property
    def behaviour_tab(self):
        return self.parentWidget()
