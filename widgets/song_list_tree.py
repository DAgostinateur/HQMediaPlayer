from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor

import audio
import util


# noinspection PyUnresolvedReferences
class SongListTree(QTreeWidget):
    GREEN_QBRUSH = QBrush(QColor(30, 190, 30))
    WHITE_QBRUSH = QBrush(QColor(255, 255, 255))

    def __init__(self, parent=None):
        super(SongListTree, self).__init__(parent)

        self.setGeometry(17, 190, 667, 221)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setHeaderHidden(False)

        self.set_song_list_header()

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_control_box(self):
        return self.parentWidget()

    def set_song_list_header(self):
        self.setHeaderLabels(["Title", "Artist", "Length", "Size"])
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 140)
        self.setColumnWidth(2, 80)

    def add_highlight(self, playlist):
        self.set_background_colour(playlist, self.GREEN_QBRUSH)

    def remove_highlight(self, playlist):
        self.set_background_colour(playlist, self.WHITE_QBRUSH)

    def set_background_colour(self, playlist: audio.WPlaylist, colour):
        item = self.topLevelItem(playlist.currentIndex())

        item.setBackground(0, colour)
        item.setBackground(1, colour)
        item.setBackground(2, colour)
        item.setBackground(3, colour)

    def update_song_list(self, playlist: audio.WPlaylist):
        self.clear()

        for i in range(0, playlist.mediaCount()):
            wsong = audio.WSong()
            wsong.set_song(playlist.get_song(i))

            item = QTreeWidgetItem(self)
            item.setText(0, wsong.get_info(audio.WSong.TITLE))
            item.setText(1, wsong.get_info(audio.WSong.ARTIST))
            item.setText(2, util.format_duration(wsong.get_real_duration()))
            item.setText(3, wsong.get_file_size())

    # def empty_song_list(self):
    #     self.title_item.
