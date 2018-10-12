from PyQt5.QtWidgets import QRadioButton


# noinspection PyArgumentList
class NothingRadioButton(QRadioButton):
    def __init__(self, parent=None):
        super(NothingRadioButton, self).__init__(parent)

        self.setGeometry(10, 40, 111, 20)
        self.setToolTip("The play button (when clicked) will do nothing.")
        self.setText("Do nothing")

        self.clicked.connect(self.nrb_clicked)

    @property
    def option_play_button_box(self):
        return self.parentWidget()

    def nrb_clicked(self):
        """Radio Nothing clicked"""
        self.option_play_button_box.behaviour_tab.options_dialog.behaviour_play_button = \
            self.option_play_button_box.behaviour_tab.options_dialog.behaviour_play_button_nothing
