from PyQt5.QtWidgets import QLabel, QFrame
from PyQt5.QtCore import Qt

import util


# noinspection PyUnresolvedReferences
class AlbumArtLabel(QLabel):
    def __init__(self, parent=None):
        super(AlbumArtLabel, self).__init__(parent)
        self.setGeometry(240, 13, 128, 128)
        self.setFrameShape(QFrame.Box)
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignHCenter)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_info_box(self):
        return self.parentWidget()
