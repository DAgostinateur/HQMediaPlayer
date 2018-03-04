import ctypes
import sys

import files
import util
from audio import WSong
from widgets import (volume_slider, mute_button, repeat_button,
                     stop_button, pause_button, play_button,
                     music_position_label, duration_slider, embedded_console)
# PyCharm doesn't understand "from widgets import *", so I don't have intellisense for every class


from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QGroupBox,
                             QMenu, QMenuBar, QAction, QStatusBar)
from PyQt5.QtGui import QKeyEvent, QCloseEvent, QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic


# TODO:
# Maybe create QPushButtons, QLabel, etc. in .py instead .ui
# Make a better looking UI
# Create a Playlist class
# QtxGlobalShortcuts, look into that


# Fixes the TaskBar Icon bug
# https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("dagostinateur_woh.hqmediaplayer.v1")


# noinspection PyCallByClass,PyArgumentList,PyUnresolvedReferences
class HQMediaPlayer(QMainWindow):
    def __init__(self, parent=None):
        super(HQMediaPlayer, self).__init__(parent)
        self.key_list = []
        self.first_release = False

        uic.loadUi(files.MAIN_WINDOW_UI, self)
        self.setWindowIcon(QIcon(files.Images.WPLAYER_LOGO))

        self.song = WSong(files.MUSIC_LETS_PRACTICE)
        self.player = QMediaPlayer()
        self.dbg_console = embedded_console.EmbeddedConsole()

        self.volume_slider = volume_slider.VolumeSlider(self.music_box)
        self.duration_slider = duration_slider.DurationSlider(self.music_box)

        self.mute_button = mute_button.MuteButton(self.music_box)
        self.repeat_button = repeat_button.RepeatButton(self.music_box)
        self.stop_button = stop_button.StopButton(self.music_box)
        self.pause_button = pause_button.PauseButton(self.music_box)
        self.play_button = play_button.PlayButton(self.music_box)

        self.music_position_label = music_position_label.MusicPositionLabel(self.music_box)

        self.create_connections()

        self.album_art_label.setScaledContents(True)

        self.player.setMedia(self.song.content)
        self.player.setVolume(self.volume_slider.default_volume)

        if False:
            # Helps for intellisense
            self.album_art_label = QLabel()
            self.artist_label = QLabel()
            self.length_label = QLabel()
            self.title_label = QLabel()

            self.music_box = QGroupBox()
            self.music_info_box = QGroupBox()

            self.main_menubar = QMenuBar()
            self.file_menu = QMenu()
            self.help_menu = QMenu()

            self.debug_console_action = QAction()

            self.main_statusbar = QStatusBar()

    def debug_console_action_triggered(self):
        if not self.dbg_console.isVisible():
            self.dbg_console.show()
        else:
            self.dbg_console.close()

    def player_position_changed(self, position):
        if not self.player.state() == QMediaPlayer.StoppedState:
            self.music_position_label.setText(util.format_duration(position))
            self.duration_slider.setValue(position)

    def player_state_changed(self, status):
        if status == QMediaPlayer.EndOfMedia and self.repeat_button.repeating:
            self.player.play()
        elif status == QMediaPlayer.EndOfMedia:
            self.reset_duration_slider()
            self.reset_music_info()
            self.duration_slider.setDisabled(True)

            self.stop_button.setToolTip("Stopped")
            self.stop_button.setIcon(QIcon(files.Images.STOPPED))
            self.play_button.setToolTip("Play")
            self.play_button.setIcon(QIcon(files.Images.PLAY))

    def set_song_info(self):
        title = self.song.get_info(WSong.TITLE)
        artist = self.song.get_info(WSong.ARTIST)
        length = util.format_duration(self.song.get_real_duration())

        self.title_label.setText(("Title  : " + title))
        self.artist_label.setText(("Artist : " + artist))
        self.length_label.setText(("Length : " + length))

        self.title_label.setToolTip(title)
        self.artist_label.setToolTip(artist)
        self.length_label.setToolTip(length)

        self.title_label.adjustSize()
        self.artist_label.adjustSize()
        self.length_label.adjustSize()

        if self.song.get_apic(True):
            self.album_art_label.setPixmap(QPixmap(files.TEMP_PNG_FILE))
            self.song.remove_apic_file()

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
        print(key_list)
        if (util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Home]) or
                util.check_keys(key_list, [Qt.Key_MediaTogglePlayPause])):
            if self.player.state() == QMediaPlayer.PlayingState:
                self.pause_button.pb_clicked()
            elif self.player.state() == QMediaPlayer.PausedState or self.player.state() == QMediaPlayer.StoppedState:
                self.play_button.plb_clicked()

        elif util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Up]):
            self.volume_slider.increase_volume(5)
        elif util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Down]):
            self.volume_slider.decrease_volume(5)
        elif util.check_keys(key_list, [Qt.Key_MediaStop]):
            self.stop_button.sb_clicked()
        elif util.check_keys(key_list, [Qt.Key_MediaPlay]):
            self.play_button.plb_clicked()
        elif util.check_keys(key_list, [Qt.Key_MediaPause]):
            self.pause_button.pb_clicked()

        if any(key_list.count(x) > 1 for x in key_list):
            del key_list[:]

    def closeEvent(self, event: QCloseEvent):
        self.dbg_console.close()

    def reset_duration_slider(self):
        self.music_position_label.reset_time()
        self.duration_slider.reset_slider()

    def reset_music_info(self):
        self.title_label.setText("Title  : ")
        self.artist_label.setText("Artist : ")
        self.length_label.setText("Length : ")
        self.album_art_label.clear()

        self.title_label.setToolTip("")
        self.artist_label.setToolTip("")
        self.length_label.setToolTip("")

    def create_connections(self):
        self.debug_console_action.triggered.connect(self.debug_console_action_triggered)

        self.player.positionChanged.connect(self.player_position_changed)
        self.player.mediaStatusChanged.connect(self.player_state_changed)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    media_player = HQMediaPlayer()
    media_player.show()
    sys.exit(app.exec_())
