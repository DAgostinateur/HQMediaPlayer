from PyQt5.QtWidgets import QLabel

import util


# noinspection PyUnresolvedReferences
class LengthLabel(QLabel):
    def __init__(self, parent=None):
        super(LengthLabel, self).__init__(parent)
        self.setGeometry(10, 55, 54, 13)
        self.setText("Length :")

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_info_box(self):
        return self.parentWidget()

    def set_length(self, length):
        self.setText(("Length : " + length))
        self.setToolTip(length)
        self.adjustSize()

    def reset_length(self):
        self.setText("Length :")
        self.setToolTip("")
