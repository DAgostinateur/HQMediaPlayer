from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

import util


# noinspection PyUnresolvedReferences
class PlaylistTotalLabel(QLabel):
    default_text = "Total of songs: "

    def __init__(self, parent=None):
        super(PlaylistTotalLabel, self).__init__(parent)
        self.setGeometry(10, 130, 218, 13)
        self.setText("{}{}".format(self.default_text, 0))
        self.setAlignment(Qt.AlignLeft)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_info_box(self):
        return self.parentWidget()

    def set_playlist_total(self):
        if self.mainwindow.music_control_box.player.has_playlist:
            self.setText("{}{}".format(self.default_text, self.mainwindow.playlist.mediaCount()))
        else:
            self.setText("{}{}".format(self.default_text, 1))

    def reset_total(self):
        self.setText("{}{}".format(self.default_text, 0))
