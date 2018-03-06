from PyQt5.QtWidgets import QLabel

import util


# noinspection PyUnresolvedReferences
class ArtistLabel(QLabel):
    def __init__(self, parent=None):
        super(ArtistLabel, self).__init__(parent)
        self.setGeometry(10, 35, 54, 13)
        self.setText("Artist :")

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_info_box(self):
        return self.parentWidget()

    def set_artist(self, artist):
        self.setText(("Artist : " + artist))
        self.setToolTip(artist)
        self.adjustSize()

    def reset_artist(self):
        self.setText("Artist :")
        self.setToolTip("")
