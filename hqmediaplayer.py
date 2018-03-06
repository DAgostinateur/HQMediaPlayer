import ctypes
import sys

import files
import util
import audio
from widgets import (music_control_box, music_info_box, embedded_console)

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QAction, QWidget)
from PyQt5.QtGui import QKeyEvent, QCloseEvent, QIcon, QFont
from PyQt5.QtCore import Qt, QSize


# TODO:
# Change TitleLabel, etc. to a Label and TextEdit combo
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

        self.setMinimumSize(702, 474)
        self.setFont(QFont("Consolas"))
        self.setWindowTitle("HQMediaPlayer")
        self.setIconSize(QSize(32, 32))
        self.setWindowIcon(QIcon(files.Images.WPLAYER_LOGO))

        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(0, 21, 702, 433)

        self.song = audio.WSong(files.MUSIC_DDD)
        self.player = QMediaPlayer()
        self.dbg_console = embedded_console.EmbeddedConsole()
        self.music_control_box = music_control_box.MusicControlBox(self.centralwidget)
        self.music_info_box = music_info_box.MusicInfoBox(self.centralwidget)

        self.create_menubar()
        self.create_connections()

        self.player.setMedia(self.song.content)
        self.player.setVolume(self.music_control_box.volume_slider.default_volume)

    def debug_console_action_triggered(self):
        if not self.dbg_console.isVisible():
            self.dbg_console.show()
        else:
            self.dbg_console.close()

    def player_position_changed(self, position):
        if not self.player.state() == QMediaPlayer.StoppedState:
            self.music_control_box.music_position_label.setText(util.format_duration(position))
            self.music_control_box.duration_slider.setValue(position)

    def player_state_changed(self, status):
        if status == QMediaPlayer.EndOfMedia and self.music_control_box.repeat_button.repeating:
            self.player.play()
        elif status == QMediaPlayer.EndOfMedia:
            self.music_control_box.reset_duration()
            self.music_info_box.reset_music_info()
            self.music_control_box.duration_slider.setDisabled(True)

            self.music_control_box.stop_button.setToolTip("Stopped")
            self.music_control_box.stop_button.setIcon(QIcon(files.Images.STOPPED))
            self.music_control_box.play_button.setToolTip("Play")
            self.music_control_box.play_button.setIcon(QIcon(files.Images.PLAY))

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
                self.music_control_box.pause_button.pb_clicked()
            elif self.player.state() == QMediaPlayer.PausedState or self.player.state() == QMediaPlayer.StoppedState:
                self.music_control_box.play_button.plb_clicked()

        elif util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Up]):
            self.music_control_box.volume_slider.increase_volume(5)
        elif util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Down]):
            self.music_control_box.volume_slider.decrease_volume(5)
        elif util.check_keys(key_list, [Qt.Key_MediaStop]):
            self.music_control_box.stop_button.sb_clicked()
        elif util.check_keys(key_list, [Qt.Key_MediaPlay]):
            self.music_control_box.play_button.plb_clicked()
        elif util.check_keys(key_list, [Qt.Key_MediaPause]):
            self.music_control_box.pause_button.pb_clicked()

        if any(key_list.count(x) > 1 for x in key_list):
            del key_list[:]

    def closeEvent(self, event: QCloseEvent):
        self.dbg_console.close()

    def create_connections(self):
        self.player.positionChanged.connect(self.player_position_changed)
        self.player.mediaStatusChanged.connect(self.player_state_changed)

    def create_menubar(self):
        debug_console_action = QAction(self)
        debug_console_action.setText("Debug Console")
        debug_console_action.setIconText("Debug Console")
        debug_console_action.setToolTip("Debug Console")
        debug_console_action.setFont(QFont("Consolas", 10))
        debug_console_action.triggered.connect(self.debug_console_action_triggered)

        file_menu = QMenu(self)
        file_menu.setTitle("File")
        file_menu.setFont(QFont("Consolas", 10))

        help_menu = QMenu(self)
        help_menu.setTitle("Help")
        help_menu.setFont(QFont("Consolas", 10))
        help_menu.addAction(debug_console_action)

        menubar = self.menuBar()
        menubar.addMenu(file_menu)
        menubar.addMenu(help_menu)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    media_player = HQMediaPlayer()
    media_player.show()
    sys.exit(app.exec_())
