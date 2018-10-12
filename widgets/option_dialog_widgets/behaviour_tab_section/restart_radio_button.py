from PyQt5.QtWidgets import QRadioButton


# noinspection PyArgumentList
class RestartRadioButton(QRadioButton):
    def __init__(self, parent=None):
        super(RestartRadioButton, self).__init__(parent)

        self.setGeometry(10, 20, 111, 20)
        self.setToolTip("The play button (when clicked) will restart the song.")
        self.setText("Restart")

        self.clicked.connect(self.srb_clicked)

    @property
    def option_play_button_box(self):
        return self.parentWidget()

    def srb_clicked(self):
        """Radio Restart clicked"""
        self.option_play_button_box.behaviour_tab.options_dialog.behaviour_play_button = \
            self.option_play_button_box.behaviour_tab.options_dialog.behaviour_play_button_restart
