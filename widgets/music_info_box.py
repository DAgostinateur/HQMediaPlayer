from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtGui import QPixmap

from widgets import (title_label, artist_label, length_label, album_art_label)

import audio
import util
import files


# noinspection PyUnresolvedReferences
class MusicInfoBox(QGroupBox):
    def __init__(self, parent=None):
        super(MusicInfoBox, self).__init__(parent)
        self.setGeometry(7, 17, 381, 155)

        self.title_label = title_label.TitleLabel(self)
        self.artist_label = artist_label.ArtistLabel(self)
        self.length_label = length_label.LengthLabel(self)
        self.album_art_label = album_art_label.AlbumArtLabel(self)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 2)

    def reset_music_info(self):
        self.title_label.reset_title()
        self.artist_label.reset_artist()
        self.length_label.reset_length()
        self.album_art_label.clear()

    def set_song_info(self):
        self.title_label.set_title(self.mainwindow.song.get_info(audio.WSong.TITLE))
        self.artist_label.set_artist(self.mainwindow.song.get_info(audio.WSong.ARTIST))
        self.length_label.set_length(util.format_duration(self.mainwindow.song.get_real_duration()))

        if self.mainwindow.song.get_apic(True):
            self.album_art_label.setPixmap(QPixmap(files.TEMP_PNG_FILE))
            self.mainwindow.song.remove_apic_file()
