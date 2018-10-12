from PyQt5.QtWidgets import QRadioButton


# noinspection PyArgumentList
class NoAutoplayRadioButton(QRadioButton):
    def __init__(self, parent=None):
        super(NoAutoplayRadioButton, self).__init__(parent)

        self.setGeometry(10, 40, 111, 20)
        self.setToolTip("It will NOT automatically start the player.")
        self.setText("No Autoplay")

        self.clicked.connect(self.narb_clicked)

    @property
    def option_playlist_autoplay_box(self):
        return self.parentWidget()

    def narb_clicked(self):
        """Radio No Autoplay clicked"""
        self.option_playlist_autoplay_box.behaviour_tab.options_dialog.behaviour_playlist_autoplay = \
            self.option_playlist_autoplay_box.behaviour_tab.options_dialog.behaviour_playlist_autoplay_nothing
