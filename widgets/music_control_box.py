from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtCore import Qt

from widgets.music_control_widgets import (pause_button, play_button, next_button, stop_button,
                                           repeat_button, previous_button, mute_button,
                                           duration_slider, volume_slider, music_position_label)

import util
import files
from audio import WMediaPlayer


# noinspection PyUnresolvedReferences
class MusicControlBox(QGroupBox):
    def __init__(self, parent=None):
        super(MusicControlBox, self).__init__(parent)
        self.setGeometry(403, 10, 291, 162)
        self.setFont(QFont("Consolas", 10))
        self.setTitle("Music Control")
        self.setAlignment(Qt.AlignHCenter)

        self.volume_slider = volume_slider.VolumeSlider(self)
        self.duration_slider = duration_slider.DurationSlider(self)

        self.mute_button = mute_button.MuteButton(self)
        self.repeat_button = repeat_button.RepeatButton(self)
        self.stop_button = stop_button.StopButton(self)
        self.pause_button = pause_button.PauseButton(self)
        self.play_button = play_button.PlayButton(self)
        self.next_button = next_button.NextButton(self)
        self.previous_button = previous_button.PreviousButton(self)

        self.music_position_label = music_position_label.MusicPositionLabel(self)

        self.player = WMediaPlayer(self)
        self.player.setVolume(self.volume_slider.volume_at_start)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 2)

    def reset_duration(self):
        self.music_position_label.reset_time()
        self.duration_slider.reset_slider()

    def toggle_play_pause(self):
        if self.player.state() == self.player.PlayingState:
            self.pause_button.pb_clicked()
        elif (self.player.state() == self.player.PausedState or
              self.player.state() == self.player.StoppedState):
            self.play_button.plb_clicked()

    def set_playing_state_buttons(self):
        self.stop_button.setToolTip("Stop")
        self.stop_button.setIcon(QIcon(files.Images.STOP))
        self.pause_button.setToolTip("Pause")
        self.pause_button.setIcon(QIcon(files.Images.PAUSE))

    def set_stopped_state_buttons(self):
        self.pause_button.setToolTip("Pause")
        self.pause_button.setIcon(QIcon(files.Images.PAUSE))
        self.play_button.setToolTip("Play")
        self.play_button.set_play_icon()

    def set_paused_state_buttons(self):
        self.play_button.setToolTip("Play")
        self.play_button.set_play_icon()

    def set_end_of_media_buttons(self):
        self.stop_button.setToolTip("Stopped")
        self.stop_button.setIcon(QIcon(files.Images.STOPPED))
        self.play_button.setToolTip("Play")
        self.play_button.set_play_icon()
