from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent
import mutagen.mp3
import os


def is_music_file(file: str):
    return os.path.isfile(file) and file.lower().endswith(('.mp3', '.wav'))


class InvalidFile(Exception):
    pass


class WSong:
    ARTIST = "artist"
    TITLE = "title"
    ALBUM = "album"

    def __init__(self, file_location: str):
        if not is_music_file(file_location):
            raise InvalidFile("{0} -- is not valid".format(file_location))

        self.metadata = mutagen.mp3.EasyMP3(file_location)
        self.content = QMediaContent(QUrl.fromLocalFile(file_location))  # For QMediaPlayer

    def get_info(self, wanted_info: str = TITLE):
        """

        :return: Returns the song's artist.
        """
        info = str(self.metadata[wanted_info])
        return info[2:len(info) - 2]  # Removes the ['']

    def get_real_duration(self):
        """

        :return: Return the song's true duration in milliseconds.
        """
        return int(self.metadata.info.length * 1000)

    def get_player_duration(self):
        """

        :return: Return the song's duration for QMediaPlayer in milliseconds.
        """
        # QMediaPlayer adds 202 milliseconds to the duration, no idea why.
        return self.get_real_duration() + 202
