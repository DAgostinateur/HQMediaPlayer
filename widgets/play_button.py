from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QFileDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtMultimedia import QMediaPlayer

import options_dialog
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
        if self.mainwindow.player.state() == QMediaPlayer.PlayingState:
            self.set_playing_icon()
        else:
            self.set_play_icon()

    def plb_released(self):
        self.clearFocus()

    def restart_player(self):
        self.mainwindow.player.stop()
        self.music_control_box.duration_slider.setEnabled(True)
        self.music_control_box.reset_duration()
        self.music_control_box.duration_slider.setMaximum(self.mainwindow.song.get_player_duration())

        self.mainwindow.music_info_box.set_song_info()
        self.mainwindow.player.play()

    def plb_clicked(self):
        if not self.mainwindow.song.has_song():
            file_name, file_type = QFileDialog.getOpenFileName(self, "Openfile", "/", "MP3 (*.mp3)")
            if ".mp3" in file_type:
                self.mainwindow.song.set_song(file_name)
                self.mainwindow.player.setMedia(self.mainwindow.song.content)
            else:
                return

        if self.mainwindow.player.state() == QMediaPlayer.PlayingState:
            if self.mainwindow.options.get_default_play_button() == \
                    options_dialog.OptionsDialog.behaviour_play_button_restart:
                self.restart_player()

        elif self.mainwindow.player.state() == QMediaPlayer.StoppedState:
            self.mainwindow.player.stop()
            self.music_control_box.duration_slider.setEnabled(True)
            self.music_control_box.reset_duration()
            self.music_control_box.duration_slider.setMaximum(self.mainwindow.song.get_player_duration())

            self.mainwindow.music_info_box.set_song_info()
            self.mainwindow.player.play()
        elif self.mainwindow.player.state() == QMediaPlayer.PausedState:
            self.mainwindow.player.play()

        self.music_control_box.set_playing_state_buttons()
        self.setToolTip("Playing")
        self.set_playing_icon()
