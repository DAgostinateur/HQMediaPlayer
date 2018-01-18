import sys
import ctypes

import files
import embedded_console
from audio import WSong

from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic


# TODO:
# Maybe create QPushButtons, QLabel, etc. in .py instead .ui
#
# Hide the console if possible
# Move the console
# Create a menu tool bar
# Make a better looking UI
# Create a Playlist class
# QtxGlobalShortcuts, look into that

# Fixes the TaskBar Icon bug
# https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("dagostinateur_woh.hqmediaplayer.v1")


def format_duration(duration: float):
    """

    :param duration: Duration in milliseconds
    :return: Duration in HOURS:MINUTES:SECONDS format
    """
    m, s = divmod(duration / 1000, 60)
    h, m = divmod(m, 60)
    if h:
        return "{0}:{1:0>2}:{2:0>2}".format(str(int(h)).zfill(2),
                                            str(int(m)).zfill(2), str(int(s)).zfill(2))
    else:
        return "{0}:{1:0>2}".format(str(int(m)).zfill(2), str(int(s)).zfill(2))


def check_keys(key_list: list, wanted_key_list: list):
    key_count = 0
    print(key_list)
    print(wanted_key_list)
    for key in key_list:
        for wanted_key in wanted_key_list:
            if key == wanted_key:
                key_count += 1
                break

    return key_count == len(wanted_key_list)


# noinspection PyCallByClass,PyArgumentList,PyUnresolvedReferences
class HQMediaPlayer(QWidget):
    muted = False
    repeating = False
    value_when_muted = 25

    key_list = []
    first_release = False

    def __init__(self, parent=None):
        super(HQMediaPlayer, self).__init__(parent)
        uic.loadUi(files.MAIN_UI, self)
        self.setFocus()
        self.setWindowIcon(QIcon(files.Images.WPLAYER_LOGO))

        self.song = WSong(files.MUSIC_MIBILIS)
        self.player = QMediaPlayer()

        self.create_connections()

        self.dbg_console = embedded_console.EmbeddedConsole(self)

        self.player.setMedia(self.song.content)
        self.player.setVolume(self.value_when_muted)

        if False:
            # Helps for intellisense
            self.dbg_console_label = QLabel()
            self.music_position_label = QLabel()
            self.music_box = QGroupBox()
            self.volume_slider = QSlider()
            self.duration_slider = QSlider()
            self.clear_console_button = QPushButton()
            self.play_button = QPushButton()
            self.pause_button = QPushButton()
            self.mute_button = QPushButton()
            self.repeat_button = QPushButton()
            self.stop_button = QPushButton()

    def duration_slider_pressed(self):
        self.player.setMuted(True)

    def duration_slider_released(self):
        self.player.setMuted(False)
        self.duration_slider.clearFocus()

    def duration_slider_moved(self, value):
        self.player.setPosition(value)

    def player_position_changed(self, position):
        if not self.player.state() == QMediaPlayer.StoppedState:
            self.music_position_label.setText(format_duration(position))
            self.duration_slider.setValue(position)

    def player_state_changed(self, status):
        if status == QMediaPlayer.EndOfMedia and self.repeating:
            self.player.play()
        elif status == QMediaPlayer.EndOfMedia:
            self.reset_duration_slider()
            self.duration_slider.setDisabled(True)
            self.set_to_stopped()
            self.set_to_play()

    def volume_slider_value_changed(self):
        self.player.setVolume(self.volume_slider.value())
        if self.muted:
            self.muted = False

        self.mute_button.setIcon(self.check_volume_value(self.volume_slider.value()))
        self.volume_slider.setToolTip(str(self.volume_slider.value()))

    def clear_console_clicked(self):
        self.dbg_console.clear()
        self.clear_console_button.clearFocus()

    def play_button_clicked(self):
        if self.player.state() == QMediaPlayer.PlayingState \
                or self.player.state() == QMediaPlayer.StoppedState:
            self.player.stop()
            self.duration_slider.setEnabled(True)
            self.reset_duration_slider()
            self.duration_slider.setMaximum(self.song.get_player_duration())

            self.dbg_console.write(
                "Title: {0}\nArtist: {1}\nAlbum: {2}\nDuration: {3}".format(
                    self.song.get_info(WSong.TITLE), self.song.get_info(WSong.ARTIST),
                    self.song.get_info(WSong.ALBUM), format_duration(self.song.get_real_duration())))
            self.player.play()
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()

        self.set_to_stop()
        self.set_to_playing()
        self.set_to_pause()

    def pause_button_clicked(self):
        if not self.player.state() == QMediaPlayer.StoppedState:
            self.player.pause()
            self.set_to_paused()
            self.set_to_play()

    def mute_button_clicked(self):
        if self.muted:
            self.set_to_unmuted()
            self.volume_slider.setValue(self.value_when_muted)
            self.muted = False
        else:
            self.value_when_muted = self.volume_slider.value()
            self.volume_slider.setValue(0)
            self.set_to_mute()
            self.muted = True

    def repeat_button_clicked(self):
        if self.repeating:
            self.set_to_repeat()
            self.repeating = False
        else:
            self.set_to_repeating()
            self.repeating = True

    def stop_button_clicked(self):
        self.player.stop()
        self.reset_duration_slider()
        self.duration_slider.setDisabled(True)
        self.set_to_stopped()
        self.set_to_pause()
        self.set_to_play()

    def keyPressEvent(self, event: QKeyEvent):
        # https://stackoverflow.com/questions/7176951/how-to-get-multiple-key-presses-in-single-event/10568233#10568233
        self.first_release = True
        self.key_list.append(int(event.key()))

    def keyReleaseEvent(self, event: QKeyEvent):
        if self.first_release:
            self.process_multi_keys(self.key_list)

        self.first_release = False
        try:
            del self.key_list[-1]
        except IndexError:
            pass

    def process_multi_keys(self, key_list):
        if (check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Home]) or
                check_keys(key_list, [Qt.Key_MediaTogglePlayPause])):
            if self.player.state() == QMediaPlayer.PlayingState:
                self.pause_button_clicked()
            elif self.player.state() == QMediaPlayer.PausedState or self.player.state() == QMediaPlayer.StoppedState:
                self.play_button_clicked()

        elif check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Up]):
            self.volume_slider.setValue(self.volume_slider.value() + 5)
        elif check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Down]):
            self.volume_slider.setValue(self.volume_slider.value() - 5)
        elif check_keys(key_list, [Qt.Key_MediaStop]):
            self.stop_button_clicked()

    @staticmethod
    def check_volume_value(value: int):
        """Checks the volume and returns the appropriate image for mute_button.

        :param value: Volume value or muted value
        :return: QIcon with appropriate image
        """
        if value < 1:
            return QIcon(files.Images.VOLUME_0)
        elif value <= 33:
            return QIcon(files.Images.VOLUME_LESS_33)
        elif value <= 66:
            return QIcon(files.Images.VOLUME_LESS_66)
        elif value <= 100:
            return QIcon(files.Images.VOLUME_LESS_100)
        else:
            return QIcon(files.Images.VOLUME_ERROR)

    def reset_duration_slider(self):
        self.music_position_label.setText("00:00")
        self.duration_slider.setValue(0)
        self.duration_slider.setMaximum(271)

    def set_to_play(self):
        self.play_button.setToolTip("Play")
        self.play_button.setIcon(QIcon(files.Images.PLAY))

    def set_to_playing(self):
        self.play_button.setToolTip("Playing")
        self.play_button.setIcon(QIcon(files.Images.PLAYING))

    def set_to_pause(self):
        self.pause_button.setToolTip("Pause")
        self.pause_button.setIcon(QIcon(files.Images.PAUSE))

    def set_to_paused(self):
        self.pause_button.setToolTip("Paused")
        self.pause_button.setIcon(QIcon(files.Images.PAUSED))

    def set_to_mute(self):
        self.mute_button.setToolTip("Muted")
        self.mute_button.setIcon(QIcon(files.Images.MUTED))

    def set_to_unmuted(self):
        self.mute_button.setToolTip("Mute")
        self.mute_button.setIcon(self.check_volume_value(self.value_when_muted))

    def set_to_repeat(self):
        self.repeat_button.setToolTip("Repeat")
        self.repeat_button.setIcon(QIcon(files.Images.REPEAT))

    def set_to_repeating(self):
        self.repeat_button.setToolTip("Repeating")
        self.repeat_button.setIcon(QIcon(files.Images.REPEATING))

    def set_to_stop(self):
        self.stop_button.setToolTip("Stop")
        self.stop_button.setIcon(QIcon(files.Images.STOP))

    def set_to_stopped(self):
        self.stop_button.setToolTip("Stopped")
        self.stop_button.setIcon(QIcon(files.Images.STOPPED))

    def create_connections(self):
        self.clear_console_button.clicked.connect(self.clear_console_clicked)

        self.play_button.clicked.connect(self.play_button_clicked)
        self.play_button.released.connect(self.play_button.clearFocus)

        self.pause_button.clicked.connect(self.pause_button_clicked)
        self.pause_button.released.connect(self.pause_button.clearFocus)

        self.mute_button.clicked.connect(self.mute_button_clicked)
        self.mute_button.released.connect(self.mute_button.clearFocus)

        self.repeat_button.clicked.connect(self.repeat_button_clicked)
        self.repeat_button.released.connect(self.repeat_button.clearFocus)

        self.stop_button.clicked.connect(self.stop_button_clicked)
        self.stop_button.released.connect(self.stop_button.clearFocus)

        self.volume_slider.valueChanged.connect(self.volume_slider_value_changed)
        self.volume_slider.sliderReleased.connect(self.volume_slider.clearFocus)

        self.duration_slider.sliderMoved.connect(self.duration_slider_moved)
        self.duration_slider.sliderPressed.connect(self.duration_slider_pressed)
        self.duration_slider.sliderReleased.connect(self.duration_slider_released)

        self.player.positionChanged.connect(self.player_position_changed)
        self.player.mediaStatusChanged.connect(self.player_state_changed)


def main():
    app = QApplication(sys.argv)
    w_media_player = HQMediaPlayer()
    w_media_player.show()
    sys.exit(app.exec_())


main()
