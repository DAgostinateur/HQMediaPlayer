from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtMultimedia import QMediaPlayer

from widgets import options_dialog
import files
import util


# noinspection PyUnresolvedReferences,PyArgumentList
class PlayButton(QPushButton):
    def __init__(self, parent=None):
        super(PlayButton, self).__init__(parent)
        self.setGeometry(216, 90, 25, 25)
        self.setToolTip("Play")
        self.setIcon(QIcon(files.Images.PLAY))
        self.setIconSize(QSize(25, 25))
        self.setFocusPolicy(Qt.ClickFocus)

        self.icon_status_hq = False

        self.released.connect(self.plb_released)
        self.clicked.connect(self.plb_clicked)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    @property
    def music_control_box(self):
        return self.parentWidget()

    def set_playing_icon(self):
        if self.icon_status_hq:
            self.setIcon(QIcon(files.Images.HQPLAYING))
        else:
            self.setIcon(QIcon(files.Images.PLAYING))

    def set_play_icon(self):
        if self.icon_status_hq:
            self.setIcon(QIcon(files.Images.HQPLAY))
        else:
            self.setIcon(QIcon(files.Images.PLAY))

    def toggle_icon_status(self):
        self.icon_status_hq = not self.icon_status_hq
        if self.music_control_box.player.state() == QMediaPlayer.PlayingState:
            self.set_playing_icon()
        else:
            self.set_play_icon()

    def plb_released(self):
        self.clearFocus()

    def restart_player(self):
        self.music_control_box.player.stop()
        self.music_control_box.duration_slider.setEnabled(True)
        self.music_control_box.reset_duration()
        self.music_control_box.duration_slider.setMaximum(self.mainwindow.song.get_player_duration())

        self.mainwindow.music_info_box.set_song_info()
        self.mainwindow.song_list_tree.add_highlight(self.mainwindow.playlist)
        self.music_control_box.player.play()

    def plb_clicked(self):
        if not self.mainwindow.song.has_song() and not self.music_control_box.player.has_playlist:
            return

        if self.music_control_box.player.state() == QMediaPlayer.PlayingState:
            if self.mainwindow.options.get_default_play_button() == \
                    options_dialog.OptionsDialog.behaviour_play_button_restart:
                self.restart_player()
        elif self.music_control_box.player.state() == QMediaPlayer.StoppedState:
            self.restart_player()
        elif self.music_control_box.player.state() == QMediaPlayer.PausedState:
            self.music_control_box.player.play()

        self.music_control_box.set_playing_state_buttons()
        self.setToolTip("Playing")
        self.set_playing_icon()
