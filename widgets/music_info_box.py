from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtGui import QPixmap

from widgets import (animated_label, album_art_label, playlist_total_label)

import audio
import util
import files


# noinspection PyUnresolvedReferences
class MusicInfoBox(QGroupBox):
    def __init__(self, parent=None):
        super(MusicInfoBox, self).__init__(parent)
        self.setGeometry(7, 17, 381, 155)

        self.playlist_total_info = playlist_total_label.PlaylistTotalLabel(self)
        self.title_info = animated_label.AnimatedLabel(self, 15, "Title  :", True)
        self.artist_info = animated_label.AnimatedLabel(self, 35, "Artist :", True)
        self.length_info = animated_label.AnimatedLabel(self, 55, "Length :", False)
        self.album_art_label = album_art_label.AlbumArtLabel(self)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 2)

    def set_timers_interval(self):
        self.title_info.timer_interval = self.mainwindow.options.get_default_timer_interval()
        self.title_info.timer.setInterval(self.title_info.timer_interval)

        self.artist_info.timer_interval = self.mainwindow.options.get_default_timer_interval()
        self.artist_info.timer.setInterval(self.artist_info.timer_interval)

        self.length_info.timer_interval = self.mainwindow.options.get_default_timer_interval()
        self.length_info.timer.setInterval(self.length_info.timer_interval)

    def reset_music_info(self):
        self.title_info.timer.stop()
        self.artist_info.timer.stop()
        self.length_info.timer.stop()

        self.playlist_total_info.reset_total()
        self.title_info.reset_label_text()
        self.artist_info.reset_label_text()
        self.length_info.reset_label_text()
        self.album_art_label.clear()

    def set_song_info(self):
        self.playlist_total_info.set_playlist_total()
        self.title_info.set_label_text(self.mainwindow.song.get_info(audio.WSong.TITLE))
        self.artist_info.set_label_text(self.mainwindow.song.get_info(audio.WSong.ARTIST))
        self.length_info.set_label_text(util.format_duration(self.mainwindow.song.get_real_duration()))

        if self.mainwindow.song.get_apic(True):
            self.album_art_label.setPixmap(QPixmap(files.TEMP_PNG_FILE))
            self.mainwindow.song.remove_apic_file()

        self.title_info.timer.start()
        self.artist_info.timer.start()
        self.length_info.timer.start()
