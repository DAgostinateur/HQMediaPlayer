from PyQt5.QtWidgets import QWidget

import util

from widgets.option_dialog_widgets.behaviour_tab_section import (option_play_button_box, option_scrolling_text_box,
                                                                 option_playlist_autoplay_box)


# noinspection PyArgumentList
class BehaviourTab(QWidget):
    def __init__(self, parent=None):
        super(BehaviourTab, self).__init__(parent)

        self.option_play_button = option_play_button_box.OptionPlayButtonBox(self)
        self.option_scrolling_text = option_scrolling_text_box.OptionScrollingTextBox(self)
        self.option_playlist_autoplay = option_playlist_autoplay_box.OptionPlaylistAutoplayBox(self)

    @property
    def options_dialog(self):
        return util.get_upper_parentwidget(self, 3)
