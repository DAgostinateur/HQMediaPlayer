from PyQt5.QtWidgets import (QWidget, QDialogButtonBox, QDialog,
                             QTabWidget, QGroupBox, QRadioButton,
                             QLabel, QSpinBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

import files
import hqmediaplayer

import os
import json


class Options(object):
    default_app_options_file = "./options.json"
    default_app_volume = 25
    default_app_timer_interval = 200
    default_app_play_button_behaviour = 1

    json_volume_name = "default_volume"
    json_timer_name = "default_timer_interval"
    json_playbutton_name = "default_play_button_behaviour"

    def __init__(self):
        self.default_user_volume = None
        self.default_user_timer_interval = None
        self.default_user_play_button_behaviour = None

        self.json_user_defaults = None

        self.get_user_defaults()

    @staticmethod
    def get_default_option(user_option, app_option):
        if user_option is None:
            return app_option
        else:
            return user_option

    def get_default_volume(self):
        return self.get_default_option(self.default_user_volume, self.default_app_volume)

    def get_default_timer_interval(self):
        return self.get_default_option(self.default_user_timer_interval, self.default_app_timer_interval)

    def get_default_play_button(self):
        return self.get_default_option(self.default_user_play_button_behaviour, self.default_app_play_button_behaviour)

    def get_user_defaults(self):
        if not os.path.exists(self.default_app_options_file):
            return

        with open(self.default_app_options_file, 'r') as file:
            if os.stat(self.default_app_options_file).st_size == 0:  # If the file is empty
                return

            self.json_user_defaults = json.load(file)

            self.default_user_volume = self.set_user_default(self.json_volume_name)
            self.default_user_timer_interval = self.set_user_default(self.json_timer_name)
            self.default_user_play_button_behaviour = self.set_user_default(self.json_playbutton_name)

            print("GET USER DEFAULTS")
            print(self.default_user_volume)
            print(self.default_user_timer_interval)
            print(self.default_user_play_button_behaviour)

    def save_user_defaults(self, volume, timer_interval, play_button_behaviour):
        if volume is None:
            volume = self.get_default_option(self.default_user_volume,
                                             self.default_app_play_button_behaviour)
        else:
            self.default_user_volume = volume

        if timer_interval is None:
            timer_interval = self.get_default_option(self.default_user_timer_interval,
                                                     self.default_app_timer_interval)
        else:
            self.default_user_timer_interval = timer_interval

        if play_button_behaviour is None:
            play_button_behaviour = self.get_default_option(self.default_user_play_button_behaviour,
                                                            self.default_app_play_button_behaviour)
        else:
            self.default_user_play_button_behaviour = play_button_behaviour

        info_dicts = {'{}'.format(self.json_volume_name): volume,
                      '{}'.format(self.json_timer_name): timer_interval,
                      '{}'.format(self.json_playbutton_name): play_button_behaviour}
        json_string = json.dumps(info_dicts, indent=4, separators=(',', ' : '))

        with open(self.default_app_options_file, 'w') as file:
            file.write(json_string)

    def set_user_default(self, option_name):
        try:
            return self.json_user_defaults[option_name]
        except KeyError:
            return None


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

        self.behaviour_play_button = self.mainwindow.options.get_default_play_button()
        self.behaviour_scrolling_text_speed = self.mainwindow.options.get_default_timer_interval()

        self.behaviour_tab = QWidget()
        self.option_play_button = QGroupBox(self.behaviour_tab)
        self.radio_nothing = QRadioButton(self.option_play_button)
        self.radio_restart = QRadioButton(self.option_play_button)
        self.option_scrolling_text = QGroupBox(self.behaviour_tab)
        self.label_description = QLabel(self.option_scrolling_text)
        self.spin_millisecond = QSpinBox(self.option_scrolling_text)
        self.create_tabs()

        self.button_box = QDialogButtonBox(self)
        self.button_box.setGeometry(20, 250, 360, 32)
        self.button_box.setStandardButtons(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        self.button_box.accepted.connect(self.button_box_accepted)
        self.button_box.rejected.connect(self.button_box_rejected)
        self.radio_nothing.clicked.connect(self.rn_clicked)
        self.radio_restart.clicked.connect(self.rr_clicked)
        self.spin_millisecond.valueChanged.connect(self.sm_value_change)

    def rn_clicked(self):
        """Radio Nothing clicked"""
        self.behaviour_play_button = self.behaviour_play_button_nothing

    def rr_clicked(self):
        """Radio Restart clicked"""
        self.behaviour_play_button = self.behaviour_play_button_restart

    def sm_value_change(self):
        """Spin Millisecond value changed"""
        self.behaviour_scrolling_text_speed = self.spin_millisecond.value()

    def update_info_choices(self):
        if self.behaviour_play_button == self.behaviour_play_button_restart:
            self.radio_restart.setChecked(True)
        else:
            self.radio_nothing.setChecked(True)

        self.spin_millisecond.setValue(self.mainwindow.options.get_default_option(
            self.mainwindow.options.default_user_timer_interval,
            self.mainwindow.options.default_app_timer_interval))

    def create_tabs(self):
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(20, 10, 360, 200)
        self.tab_widget.resize(360, 200)

        self.behaviour_tab.setGeometry(0, 0, 354, 167)

        self.option_play_button.setGeometry(10, 10, 131, 71)
        self.option_play_button.setToolTip("When a song is playing, the play button (when clicked) will...")
        self.option_play_button.setTitle("Play Button")

        self.radio_nothing.setGeometry(10, 40, 111, 20)
        self.radio_nothing.setToolTip("The play button (when clicked) will do nothing.")
        self.radio_nothing.setText("Do nothing")

        self.radio_restart.setGeometry(10, 20, 111, 20)
        self.radio_restart.setToolTip("The play button (when clicked) will restart the song.")
        self.radio_restart.setText("Restart")

        self.option_scrolling_text.setGeometry(10, 85, 131, 81)
        self.option_scrolling_text.setTitle("Scrolling Text")

        self.label_description.setGeometry(10, 20, 47, 45)
        self.label_description.setToolTip("1000 millisecond = One character per second")
        self.label_description.setText("Scroll Speed (ms)")
        self.label_description.setWordWrap(True)

        self.spin_millisecond.setGeometry(70, 30, 57, 21)
        self.spin_millisecond.setMaximum(9999)
        self.spin_millisecond.setDisplayIntegerBase(10)

        self.tab_widget.addTab(self.behaviour_tab, "Behaviour")

    def button_box_accepted(self):
        self.mainwindow.options.save_user_defaults(None, self.behaviour_scrolling_text_speed,
                                                   self.behaviour_play_button)
        self.mainwindow.music_info_box.set_timer_interval()
        self.close()

    def button_box_rejected(self):
        self.close()
