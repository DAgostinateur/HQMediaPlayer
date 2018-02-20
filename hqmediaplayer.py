import ctypes

import files
import embedded_console
from audio import WSong
from widgets.volume_slider import VolumeSlider

from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic


# TODO:
# Maybe create QPushButtons, QLabel, etc. in .py instead .ui
# Add labels for Title, Artist, etc.
# Make a better looking UI
# Create a Playlist class
# QtxGlobalShortcuts, look into that

# Fixes the TaskBar Icon bug
# https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105


ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("dagostinateur_woh.hqmediaplayer.v1")


def format_duration(duration: float):
    """Formats the duration (milliseconds) to a human readable way.

    :param duration: Duration in milliseconds
    :return: Duration in HOURS:MINUTES:SECONDS format. Example: 01:05:10
    """
    m, s = divmod(duration / 1000, 60)
    h, m = divmod(m, 60)
    if h:
        return "{0}:{1:0>2}:{2:0>2}".format(str(int(h)).zfill(2),
                                            str(int(m)).zfill(2), str(int(s)).zfill(2))
    else:
        return "{0}:{1:0>2}".format(str(int(m)).zfill(2), str(int(s)).zfill(2))


def check_keys(key_list: list, wanted_key_list: list):
    """Checks if the key list has every wanted key pressed (not in order).

    :param key_list: List of keys pressed.
    :param wanted_key_list: List of keys that needs to be pressed.
    :return: Returns whether the list of keys matches the wanted list.
    """
    valid_key_count = 0
    for wanted_key in wanted_key_list:
        if any(wanted_key == key for key in key_list):
            valid_key_count += 1

    return valid_key_count == len(wanted_key_list)


# noinspection PyCallByClass,PyArgumentList,PyUnresolvedReferences
class HQMediaPlayer(QMainWindow):

    def __init__(self, parent=None):
        super(HQMediaPlayer, self).__init__(parent)
        self.muted = False
        self.repeating = False

        self.key_list = []
        self.first_release = False

        uic.loadUi(files.MAIN_WINDOW_UI, self)
        self.setWindowIcon(QIcon(files.Images.WPLAYER_LOGO))

        self.song = WSong(files.MUSIC_LETS_PRACTICE)
        self.player = QMediaPlayer()
        self.dbg_console = embedded_console.EmbeddedConsole()
        self.volume_slider = VolumeSlider(self.music_box)
        self.create_connections()

        self.album_art_label.setScaledContents(True)

        self.player.setMedia(self.song.content)
        self.player.setVolume(self.volume_slider.default_volume)

        self.play_button.setFocusPolicy(Qt.ClickFocus)
        self.pause_button.setFocusPolicy(Qt.ClickFocus)
        self.mute_button.setFocusPolicy(Qt.ClickFocus)
        self.repeat_button.setFocusPolicy(Qt.ClickFocus)
        self.stop_button.setFocusPolicy(Qt.ClickFocus)

        if False:
            # Helps for intellisense
            self.music_position_label = QLabel()
            self.album_art_label = QLabel()
            self.artist_label = QLabel()
            self.length_label = QLabel()
            self.title_label = QLabel()

            self.music_box = QGroupBox()
            self.music_info_box = QGroupBox()

            self.duration_slider = QSlider()

            self.play_button = QPushButton()
            self.pause_button = QPushButton()
            self.mute_button = QPushButton()
            self.repeat_button = QPushButton()
            self.stop_button = QPushButton()

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

    def duration_slider_pressed(self):
        self.player.setMuted(True)

    def duration_slider_moved(self, value):
        self.player.setPosition(value)

    def duration_slider_released(self):
        self.player.setMuted(False)
        self.duration_slider.clearFocus()

    def player_position_changed(self, position):
        if not self.player.state() == QMediaPlayer.StoppedState:
            self.music_position_label.setText(format_duration(position))
            self.duration_slider.setValue(position)

    def player_state_changed(self, status):
        if status == QMediaPlayer.EndOfMedia and self.repeating:
            self.player.play()
        elif status == QMediaPlayer.EndOfMedia:
            self.reset_duration_slider()
            self.reset_music_info()
            self.duration_slider.setDisabled(True)
            self.set_button_displayed_info([self.stop_button, "Stopped", files.Images.STOPPED],
                                           [self.play_button, "Play", files.Images.PLAY])

    def play_button_clicked(self):
        if self.player.state() == QMediaPlayer.PlayingState \
                or self.player.state() == QMediaPlayer.StoppedState:
            self.player.stop()
            self.duration_slider.setEnabled(True)
            self.reset_duration_slider()
            self.duration_slider.setMaximum(self.song.get_player_duration())

            title = self.song.get_info(WSong.TITLE)
            artist = self.song.get_info(WSong.ARTIST)
            length = format_duration(self.song.get_real_duration())

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

            self.player.play()
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()

        self.set_button_displayed_info([self.stop_button, "Stop", files.Images.STOP],
                                       [self.play_button, "Playing", files.Images.PLAYING],
                                       [self.pause_button, "Pause", files.Images.PAUSE])

    def pause_button_clicked(self):
        if not self.player.state() == QMediaPlayer.StoppedState:
            self.player.pause()
            self.set_button_displayed_info([self.pause_button, "Paused", files.Images.PAUSED],
                                           [self.play_button, "Play", files.Images.PLAY])

    def mute_button_clicked(self):
        if self.muted:
            self.set_button_displayed_info([self.mute_button, "Muted",
                                            self.volume_slider.get_volume_icon()])
            self.volume_slider.before_mute_volume()
            self.muted = False
        else:
            self.volume_slider.set_volume_when_muted()
            self.volume_slider.mute_volume()
            self.set_button_displayed_info([self.mute_button, "Mute", files.Images.MUTED])
            self.muted = True

    def repeat_button_clicked(self):
        if self.repeating:
            self.set_button_displayed_info([self.repeat_button, "Repeat", files.Images.REPEAT])
            self.repeating = False
        else:
            self.set_button_displayed_info([self.repeat_button, "Repeating", files.Images.REPEATING])
            self.repeating = True

    def stop_button_clicked(self):
        self.player.stop()
        self.reset_duration_slider()
        self.reset_music_info()
        self.duration_slider.setDisabled(True)
        self.set_button_displayed_info([self.stop_button, "Stopped", files.Images.STOPPED],
                                       [self.pause_button, "Pause", files.Images.PAUSE],
                                       [self.play_button, "Play", files.Images.PLAY])

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
        if (check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Home]) or
                check_keys(key_list, [Qt.Key_MediaTogglePlayPause])):
            if self.player.state() == QMediaPlayer.PlayingState:
                self.pause_button_clicked()
            elif self.player.state() == QMediaPlayer.PausedState or self.player.state() == QMediaPlayer.StoppedState:
                self.play_button_clicked()

        elif check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Up]):
            self.volume_slider.increase_volume(5)
        elif check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Down]):
            self.volume_slider.decrease_volume(5)
        elif check_keys(key_list, [Qt.Key_MediaStop]):
            self.stop_button_clicked()

        if any(key_list.count(x) > 1 for x in key_list):
            del key_list[:]

    def closeEvent(self, event: QCloseEvent):
        self.dbg_console.close()

    def set_button_displayed_info(self, *args):
        """Set a button's Tooltip and Icon to something different.

           A list must contain these in order:
           0 - button
           1 - tooltip
           2 - image

        :param args: Any number of list
        """
        for arg in args:
            try:
                button = arg[0]
                tooltip = arg[1]
                image = arg[2]
            except IndexError:
                self.dbg_console.write("set_button_displayed_info() failed, index invalid:")
                continue

            try:
                button.setToolTip(str(tooltip))
                if isinstance(image, QIcon):
                    button.setIcon(image)
                else:
                    button.setIcon(QIcon(image))
            except AttributeError:
                self.dbg_console.write("set_button_displayed_info() failed, arg invalid:"
                                       "\n  [{0}, '{1}', {2}]".format(str(button), str(tooltip), str(image)))

    def reset_duration_slider(self):
        self.music_position_label.setText("00:00")
        self.duration_slider.setValue(0)
        self.duration_slider.setMaximum(271)

    def reset_music_info(self):
        self.title_label.setText("Title  : ")
        self.artist_label.setText("Artist : ")
        self.length_label.setText("Length : ")
        self.album_art_label.clear()

    def create_connections(self):
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

        self.duration_slider.sliderMoved.connect(self.duration_slider_moved)
        self.duration_slider.sliderPressed.connect(self.duration_slider_pressed)
        self.duration_slider.sliderReleased.connect(self.duration_slider_released)

        self.debug_console_action.triggered.connect(self.debug_console_action_triggered)

        self.player.positionChanged.connect(self.player_position_changed)
        self.player.mediaStatusChanged.connect(self.player_state_changed)


def start_application():
    import sys
    app = QApplication(sys.argv)
    media_player = HQMediaPlayer()
    media_player.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_application()
