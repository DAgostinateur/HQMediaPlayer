from PyQt5.QtWidgets import (QWidget, QDialogButtonBox, QDialog, QTabWidget,
                             QPushButton, QGroupBox, QRadioButton,
                             QLabel, QSpinBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

import files
import util
import hqmediaplayer

import json

class Options(object):
    default_app_timer_interval = 200
    default_app_volume = 25
    default_app_play_button_behaviour = 1

    def __init__(self):
        self.default_user_volume = None
        self.default_user_timer_interval = None
        self.default_user_play_button_behaviour = None
        self.get_user_defaults()

    def get_user_defaults(self):
        pass

    def save_user_defaults(self):
        pass

# noinspection PyUnresolvedReferences,PyArgumentList
class OptionsDialog(QDialog):
    behaviour_play_button_restart = 1
    behaviour_play_button_nothing = 2

    def __init__(self, main_parent: hqmediaplayer.HQMediaPlayer = None):
        super(OptionsDialog, self).__init__()
        self.mainwindow = main_parent

        self.setGeometry(50, 50, 400, 300)
        self.setMinimumSize(400, 300)
        self.setFont(QFont("Consolas", 10))
        self.setWindowTitle("Options")
        self.setWindowIcon(QIcon(files.Images.HQPLAYER_LOGO))
        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))

        self.behaviour_play_button = self.behaviour_play_button_restart
        self.behaviour_scrolling_text_speed = self.mainwindow.music_info_box.timer_interval

        self.create_tabs()

        self.button_box = QDialogButtonBox(self)
        self.button_box.setGeometry(20, 250, 360, 32)
        self.button_box.setStandardButtons(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        self.button_box.accepted.connect(self.button_box_accepted)
        self.button_box.rejected.connect(self.button_box_rejected)

    def create_tabs(self):
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(20, 10, 360, 200)
        self.tab_widget.resize(360, 200)

        behaviour_tab = QWidget()
        behaviour_tab.setGeometry(0, 0, 354, 167)

        option_play_button = QGroupBox(behaviour_tab)
        option_play_button.setGeometry(10, 10, 131, 71)
        option_play_button.setToolTip("When a song is playing, the play button (when clicked) will...")
        option_play_button.setTitle("Play Button")

        radio_nothing = QRadioButton(option_play_button)
        radio_nothing.setGeometry(10, 40, 111, 20)
        radio_nothing.setToolTip("The play button (when clicked) will do nothing.")
        radio_nothing.setText("Do nothing")
        radio_nothing.setChecked(False)

        radio_restart = QRadioButton(option_play_button)
        radio_restart.setGeometry(10, 20, 111, 20)
        radio_restart.setToolTip("The play button (when clicked) will restart the song.")
        radio_restart.setText("Restart nothing")
        radio_restart.setChecked(False)

        option_scrolling_text = QGroupBox(behaviour_tab)
        option_scrolling_text.setGeometry(10, 85, 131, 81)
        option_scrolling_text.setTitle("Scrolling Text")

        label_description = QLabel(option_scrolling_text)
        label_description.setGeometry(10, 20, 47, 45)
        label_description.setToolTip("1000 millisecond = One character per second")
        label_description.setText("Scroll Speed (ms)")
        label_description.setWordWrap(True)

        spin_millisecond = QSpinBox(option_scrolling_text)
        spin_millisecond.setGeometry(70, 30, 57, 21)
        spin_millisecond.setMaximum(9999)
        spin_millisecond.setDisplayIntegerBase(10)

        self.tab_widget.addTab(behaviour_tab, "Behaviour")

    def button_box_accepted(self):
        self.close()

    def button_box_rejected(self):
        self.close()
