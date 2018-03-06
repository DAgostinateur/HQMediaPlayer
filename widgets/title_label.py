from PyQt5.QtWidgets import QLabel

import util


# noinspection PyUnresolvedReferences
class TitleLabel(QLabel):
    def __init__(self, parent=None):
        super(TitleLabel, self).__init__(parent)
        self.setGeometry(10, 15, 48, 13)
        self.setText("Title  :")

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_info_box(self):
        return self.parentWidget()

    def set_title(self, title):
        self.setText(("Title  : " + title))
        self.setToolTip(title)
        self.adjustSize()

    def reset_title(self):
        self.setText("Title  :")
        self.setToolTip("")
