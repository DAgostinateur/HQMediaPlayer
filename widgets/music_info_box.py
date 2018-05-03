from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

from widgets import (animated_label, album_art_label)

import audio
import util
import files


# noinspection PyUnresolvedReferences
class MusicInfoBox(QGroupBox):
    default_timer_interval = 200

    def __init__(self, parent=None):
        super(MusicInfoBox, self).__init__(parent)
        self.setGeometry(7, 17, 381, 155)

        self.title_info = animated_label.AnimatedLabel(self, 15, "Title  :", True)
        self.artist_info = animated_label.AnimatedLabel(self, 35, "Artist :", True)
        self.length_info = animated_label.AnimatedLabel(self, 55, "Length :", False)
        self.album_art_label = album_art_label.AlbumArtLabel(self)

        self.timer_interval = self.default_timer_interval

        self.timer = QTimer()
        self.timer.setInterval(self.timer_interval)
        self.timer.timeout.connect(self.animate_info)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 2)

    def reset_music_info(self):
        self.timer.stop()

        self.title_info.reset_label_text()
        self.artist_info.reset_label_text()
        self.length_info.reset_label_text()
        self.album_art_label.clear()

    def animate_info(self):
        self.title_info.animate_label_text()
        self.artist_info.animate_label_text()
        self.length_info.animate_label_text()

    def set_song_info(self):
        self.title_info.set_label_text(self.mainwindow.song.get_info(audio.WSong.TITLE))
        self.artist_info.set_label_text(self.mainwindow.song.get_info(audio.WSong.ARTIST))
        self.length_info.set_label_text(util.format_duration(self.mainwindow.song.get_real_duration()))

        if self.mainwindow.song.get_apic(True):
            self.album_art_label.setPixmap(QPixmap(files.TEMP_PNG_FILE))
            self.mainwindow.song.remove_apic_file()

        self.timer.start()
