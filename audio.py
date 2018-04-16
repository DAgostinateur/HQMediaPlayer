from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent
import mutagen.mp3
import os
import files


def is_music_file(file: str):
    return os.path.isfile(file) and file.lower().endswith(('.mp3', '.wav'))


class InvalidFile(Exception):
    pass


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
