from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlaylist, QMediaPlayer

import mutagen.mp3
import os

import files
import util


def is_music_file(file: str):
    return os.path.isfile(file) and file.lower().endswith('.mp3')


class InvalidFile(Exception):
    pass


class WMediaPlayer(QMediaPlayer):
    def __init__(self, parent=None):
        super(WMediaPlayer, self).__init__(parent)
        self.mainwindow = parent.mainwindow

        self.stateChanged.connect(self.state_changed)
        self.positionChanged.connect(self.position_changed)
        self.mediaStatusChanged.connect(self.media_status_changed)

    # @property
    # def mainwindow(self):
    #     return util.get_upper_parentwidget(self, 3)

    # @property
    # def music_control_box(self):
    #     return self.parentWidget()

    def state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.mainwindow.set_drpc_activity("Stopped")
        elif state == QMediaPlayer.PlayingState:
            self.mainwindow.set_drpc_activity("Playing")
        elif state == QMediaPlayer.PausedState:
            self.mainwindow.set_drpc_activity("Paused")
        else:
            self.mainwindow.set_drpc_activity("Broken?")

    def position_changed(self, position):
        if not self.state() == QMediaPlayer.StoppedState:
            self.mainwindow.music_control_box.music_position_label.setText(util.format_duration(position))
            self.mainwindow.music_control_box.duration_slider.setValue(position)

    def media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia and self.mainwindow.music_control_box.repeat_button.repeating:
            self.player.play()
        elif status == QMediaPlayer.EndOfMedia and self.mainwindow.has_playlist:
            self.mainwindow.playlist.setCurrentIndex(self.mainwindow.playlist.currentIndex() + 1)
            self.mainwindow.song.set_song(self.mainwindow.playlist.get_current_song())

            self.mainwindow.music_control_box.reset_duration()
            self.mainwindow.music_control_box.duration_slider.setMaximum(self.mainwindow.song.get_player_duration())
            self.mainwindow.music_info_box.set_song_info()

            self.mainwindow.set_drpc_activity("Playing")
        elif status == QMediaPlayer.EndOfMedia:
            self.mainwindow.music_control_box.reset_duration()
            self.mainwindow.music_control_box.duration_slider.setDisabled(True)

            self.mainwindow.music_control_box.set_end_of_media_buttons()


# noinspection PyArgumentList
class WPlaylist(QMediaPlaylist):
    def __init__(self, parent=None):
        super(WPlaylist, self).__init__(None)

        self.mainwindow = parent

    def get_current_song(self):
        return self.currentMedia().canonicalUrl().path()[1:]

    def set_playlist_files(self):
        for folder in self.mainwindow.options.user_music_folders:
            for file in os.listdir(folder):
                if is_music_file(os.path.join(folder, file)):
                    self.addMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(folder, file))))


# noinspection PyArgumentList
class WSong:
    ARTIST = "artist"
    TITLE = "title"
    ALBUM = "album"

    def __init__(self):
        self.file_location = None
        self.mp3 = None
        self.content = None  # For QMediaPlayer

    def set_song(self, file_location: str):
        self.file_location = file_location
        self.mp3 = mutagen.mp3.EasyMP3(file_location)
        self.content = QMediaContent(QUrl.fromLocalFile(file_location))

    def has_song(self):
        return not self.file_location is None

    def get_info(self, wanted_info: str = TITLE):
        """Gets the desired metadata from the mp3 file.

        :return: Metadata in string form.
        """
        try:
            info = str(self.mp3[wanted_info])
            return info[2:len(info) - 2]  # Removes the ['']
        except KeyError:
            return "N/A"

    def get_apic(self, file_output=False):
        """Extracts album art from a given MP3 file.  Output is raw JPEG data.

        :return: False if mp3 can't be opened, and None if no art was found
        """
        # https://uploads.s.zeid.me/python/apic-extract.py

        try:
            tags = mutagen.mp3.Open(self.file_location)
        except mutagen.MutagenError:
            return False
        data = b""
        for i in tags:
            if i.startswith("APIC"):
                data = tags[i].data
                break
        if not data:
            return None

        if file_output:
            with open(files.TEMP_PNG_FILE, 'bw') as out:
                out.write(data)
            return True

        return data

    @staticmethod
    def remove_apic_file():
        os.remove(files.TEMP_PNG_FILE)

    def get_real_duration(self):
        """

        :return: The song's true duration in milliseconds.
        """
        return int(self.mp3.info.length * 1000)

    def get_player_duration(self):
        """

        :return: The song's duration for QMediaPlayer in milliseconds.
        """
        # QMediaPlayer adds 202 milliseconds to the duration, no idea why.
        return self.get_real_duration() + 202
