from PyQt5.QtWidgets import QRadioButton


# noinspection PyArgumentList
class AutoplayRadioButton(QRadioButton):
    def __init__(self, parent=None):
        super(AutoplayRadioButton, self).__init__(parent)

        self.setGeometry(10, 20, 111, 20)
        self.setToolTip("It will automatically start the player.")
        self.setText("Autoplay")

        self.clicked.connect(self.arb_clicked)

    @property
    def option_playlist_autoplay_box(self):
        return self.parentWidget()

    def arb_clicked(self):
        """Radio Autoplay clicked"""
        self.option_playlist_autoplay_box.behaviour_tab.options_dialog.behaviour_playlist_autoplay = \
            self.option_playlist_autoplay_box.behaviour_tab.options_dialog.behaviour_playlist_autoplay_start
