from PyQt5.QtWidgets import (QWidget, QDialogButtonBox, QDialog,
                             QTabWidget, QGroupBox, QRadioButton,
                             QLabel, QSpinBox, QComboBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QAudio, QAudioDeviceInfo

import files
import hqmediaplayer
import util

import os
import json


# noinspection PyArgumentList
class Options(object):
    default_app_options_file = "./options.json"
    default_app_volume = 25
    default_app_timer_interval = 200
    default_app_play_button_behaviour = 1
    default_app_last_folder_opened = "/"
    default_app_playlist_autoplay = 1
    default_app_output_device = QAudioDeviceInfo.defaultOutputDevice().deviceName()

    json_volume_name = "default_volume"
    json_timer_name = "default_timer_interval"
    json_play_button_name = "default_play_button_behaviour"
    json_music_folders_name = "music_folders"
    json_last_folder_opened_name = "default_last_folder_opened"
    json_playlist_autoplay = "default_playlist_autoplay"
    json_output_device = "default_output_device"

    def __init__(self):
        self.default_user_volume = None
        self.default_user_timer_interval = None
        self.default_user_play_button_behaviour = None
        self.user_music_folders = None
        self.default_user_last_folder_opened = None
        self.default_user_playlist_autoplay = None
        self.default_user_output_device = None

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

    def get_default_last_folder_opened(self):
        return self.get_default_option(self.default_user_last_folder_opened, self.default_app_last_folder_opened)

    def get_default_playlist_autoplay(self):
        return self.get_default_option(self.default_user_playlist_autoplay, self.default_app_playlist_autoplay)

    def get_default_output_device(self):
        return self.get_default_option(self.default_user_output_device, self.default_app_output_device)

    def get_user_defaults(self):
        if not os.path.exists(self.default_app_options_file):
            return

        with open(self.default_app_options_file, 'r') as file:
            if os.stat(self.default_app_options_file).st_size == 0:  # If the file is empty
                return

            self.json_user_defaults = json.load(file)

            self.default_user_volume = self.set_user_default(self.json_volume_name)
            self.default_user_timer_interval = self.set_user_default(self.json_timer_name)
            self.default_user_play_button_behaviour = self.set_user_default(self.json_play_button_name)
            self.user_music_folders = self.set_user_default(self.json_music_folders_name)
            self.default_user_last_folder_opened = self.set_user_default(self.json_last_folder_opened_name)
            self.default_user_playlist_autoplay = self.set_user_default(self.json_playlist_autoplay)
            self.default_user_output_device = self.set_user_default(self.json_output_device)

    def save_user_defaults(self, volume=None, timer_interval=None, play_button_behaviour=None, music_folder=None,
                           last_folder_opened=None, playlist_autoplay=None, output_device=None):
        if volume is None:
            volume = self.get_default_volume()
        else:
            self.default_user_volume = volume

        if timer_interval is None:
            timer_interval = self.get_default_timer_interval()
        else:
            self.default_user_timer_interval = timer_interval

        if play_button_behaviour is None:
            play_button_behaviour = self.get_default_play_button()
        else:
            self.default_user_play_button_behaviour = play_button_behaviour

        if music_folder is not None:
            if self.user_music_folders is None:
                # list(self.user_music_folders).append(music_folder)
                self.user_music_folders = [music_folder]
            else:
                self.user_music_folders.append(music_folder)

        if last_folder_opened is None:
            last_folder_opened = self.get_default_last_folder_opened()
        else:
            self.default_user_last_folder_opened = last_folder_opened

        if playlist_autoplay is None:
            playlist_autoplay = self.get_default_playlist_autoplay()
        else:
            self.default_user_playlist_autoplay = playlist_autoplay

        if output_device is None:
            output_device = self.get_default_output_device()
        else:
            self.default_user_output_device = output_device

        info_dicts = {'{}'.format(self.json_volume_name): volume,
                      '{}'.format(self.json_timer_name): timer_interval,
                      '{}'.format(self.json_play_button_name): play_button_behaviour,
                      self.json_music_folders_name: self.user_music_folders,
                      '{}'.format(self.json_last_folder_opened_name): last_folder_opened,
                      '{}'.format(self.json_playlist_autoplay): playlist_autoplay,
                      '{}'.format(self.json_output_device): output_device}
        json_string = json.dumps(info_dicts, indent=4, separators=(',', ' : '))

        with open(self.default_app_options_file, 'w') as file:
            file.write(json_string)

    def delete_music_folder(self, folder):
        try:
            self.user_music_folders.remove(folder)
        except ValueError:
            return
        info_dicts = {'{}'.format(self.json_volume_name): self.default_user_volume,
                      '{}'.format(self.json_timer_name): self.default_user_timer_interval,
                      '{}'.format(self.json_play_button_name): self.default_user_play_button_behaviour,
                      self.json_music_folders_name: self.user_music_folders,
                      '{}'.format(self.json_last_folder_opened_name): self.default_user_last_folder_opened,
                      '{}'.format(self.json_playlist_autoplay): self.default_user_playlist_autoplay,
                      '{}'.format(self.json_output_device): self.default_user_output_device}
        json_string = json.dumps(info_dicts, indent=4, separators=(',', ' : '))

        with open(self.default_app_options_file, 'w') as file:
            file.write(json_string)

    def set_user_default(self, option_name):
        try:
            return self.json_user_defaults[option_name]
        except KeyError:
            return None


# noinspection PyUnresolvedReferences,PyArgumentList,PyAttributeOutsideInit
class OptionsDialog(QDialog):
    behaviour_play_button_restart = 1
    behaviour_play_button_nothing = 2

    behaviour_playlist_autoplay_start = 1
    behaviour_playlist_autoplay_nothing = 2

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
        self.behaviour_playlist_autoplay = self.mainwindow.options.get_default_playlist_autoplay()
        self.behaviour_scrolling_text_speed = self.mainwindow.options.get_default_timer_interval()
        self.audio_output_device = self.mainwindow.options.get_default_output_device()

        self.behaviour_tab = QWidget()
        self.option_play_button = QGroupBox(self.behaviour_tab)
        self.radio_nothing = QRadioButton(self.option_play_button)
        self.radio_restart = QRadioButton(self.option_play_button)
        self.option_scrolling_text = QGroupBox(self.behaviour_tab)
        self.label_description = QLabel(self.option_scrolling_text)
        self.spin_millisecond = QSpinBox(self.option_scrolling_text)
        self.option_playlist_autoplay = QGroupBox(self.behaviour_tab)
        self.radio_autoplay = QRadioButton(self.option_playlist_autoplay)
        self.radio_no_autoplay = QRadioButton(self.option_playlist_autoplay)

        self.audio_tab = QWidget()
        self.option_output_device = QGroupBox(self.audio_tab)
        self.label_selected_device = QLabel(self.option_output_device)
        self.combo_box_selected_device = QComboBox(self.option_output_device)

        self.create_tabs()

        self.button_box = QDialogButtonBox(self)
        self.button_box.setGeometry(20, 250, 360, 32)
        self.button_box.setStandardButtons(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        self.button_box.accepted.connect(self.button_box_accepted)
        self.button_box.rejected.connect(self.button_box_rejected)
        self.radio_nothing.clicked.connect(self.rn_clicked)
        self.radio_restart.clicked.connect(self.rr_clicked)
        self.spin_millisecond.valueChanged.connect(self.sm_value_change)
        self.radio_autoplay.clicked.connect(self.ra_clicked)
        self.radio_no_autoplay.clicked.connect(self.rna_clicked)
        self.combo_box_selected_device.currentIndexChanged.connect(self.cbsd_current_index_changed)

    def rn_clicked(self):
        """Radio Nothing clicked"""
        self.behaviour_play_button = self.behaviour_play_button_nothing

    def rr_clicked(self):
        """Radio Restart clicked"""
        self.behaviour_play_button = self.behaviour_play_button_restart

    def sm_value_change(self):
        """Spin Millisecond value changed"""
        self.behaviour_scrolling_text_speed = self.spin_millisecond.value()

    def ra_clicked(self):
        """Radio Autoplay clicked"""
        self.behaviour_playlist_autoplay = self.behaviour_playlist_autoplay_start

    def rna_clicked(self):
        """Radio No Autoplay clicked"""
        self.behaviour_playlist_autoplay = self.behaviour_playlist_autoplay_nothing

    def cbsd_current_index_changed(self, index):
        self.audio_output_device = self.combo_box_selected_device.itemText(index)

    def update_info_choices(self):
        if self.behaviour_play_button == self.behaviour_play_button_restart:
            self.radio_restart.setChecked(True)
        else:
            self.radio_nothing.setChecked(True)

        if self.behaviour_playlist_autoplay == self.behaviour_playlist_autoplay_start:
            self.radio_autoplay.setChecked(True)
        else:
            self.radio_no_autoplay.setChecked(True)

        self.spin_millisecond.setValue(self.mainwindow.options.get_default_option(
            self.mainwindow.options.default_user_timer_interval,
            self.mainwindow.options.default_app_timer_interval))

        self.label_selected_device.setText("Current: {}".format(self.mainwindow.options.get_default_output_device()))

        self.combo_box_selected_device.clear()
        for device in QAudioDeviceInfo.availableDevices(QAudio.AudioOutput):
            self.combo_box_selected_device.addItem(device.deviceName())
            if self.combo_box_selected_device.count() == len(QAudioDeviceInfo.availableDevices(QAudio.AudioOutput)) / 2:
                self.combo_box_selected_device.addItem(self.mainwindow.options.default_app_output_device)
                break
        for text, index in util.get_all_combo_box_items(self.combo_box_selected_device):
            if text == self.mainwindow.options.get_default_output_device():
                self.combo_box_selected_device.setCurrentIndex(index)
        self.label_selected_device.setToolTip(self.mainwindow.options.get_default_output_device())

    def create_tabs(self):
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(20, 10, 360, 200)
        self.tab_widget.resize(360, 200)

        self.behaviour_tab.setGeometry(0, 0, 354, 167)

        self.option_play_button.setGeometry(10, 10, 131, 71)
        self.option_play_button.setToolTip("When a song is playing, the play button (when clicked) will...")
        self.option_play_button.setTitle("Play Button")
        self.option_play_button.setAlignment(Qt.AlignCenter)

        self.radio_nothing.setGeometry(10, 40, 111, 20)
        self.radio_nothing.setToolTip("The play button (when clicked) will do nothing.")
        self.radio_nothing.setText("Do nothing")

        self.radio_restart.setGeometry(10, 20, 111, 20)
        self.radio_restart.setToolTip("The play button (when clicked) will restart the song.")
        self.radio_restart.setText("Restart")

        self.option_scrolling_text.setGeometry(10, 85, 131, 81)
        self.option_scrolling_text.setTitle("Scrolling Text")
        self.option_scrolling_text.setAlignment(Qt.AlignCenter)

        self.label_description.setGeometry(10, 20, 47, 45)
        self.label_description.setToolTip("1000 millisecond = One character per second")
        self.label_description.setText("Scroll Speed (ms)")
        self.label_description.setWordWrap(True)

        self.spin_millisecond.setGeometry(70, 30, 57, 21)
        self.spin_millisecond.setMaximum(9999)
        self.spin_millisecond.setDisplayIntegerBase(10)

        self.option_playlist_autoplay.setGeometry(150, 10, 131, 71)
        self.option_playlist_autoplay.setToolTip("When starting the playlist, it will...")
        self.option_playlist_autoplay.setTitle("Playlist Autoplay")
        self.option_playlist_autoplay.setAlignment(Qt.AlignCenter)

        self.radio_autoplay.setGeometry(10, 20, 111, 20)
        self.radio_autoplay.setToolTip("It will automatically start the player.")
        self.radio_autoplay.setText("Autoplay")

        self.radio_no_autoplay.setGeometry(10, 40, 111, 20)
        self.radio_no_autoplay.setToolTip("It will NOT automatically start the player.")
        self.radio_no_autoplay.setText("No Autoplay")

        self.option_output_device.setGeometry(10, 10, 331, 71)
        self.option_output_device.setToolTip("")
        self.option_output_device.setTitle("Audio Output Device (Doesn't work)")
        self.option_output_device.setAlignment(Qt.AlignCenter)

        self.label_selected_device.setGeometry(10, 17, 311, 16)
        self.label_selected_device.setToolTip("N/A")
        self.label_selected_device.setText("Current: N/A")

        self.combo_box_selected_device.setGeometry(10, 40, 311, 21)

        self.tab_widget.addTab(self.behaviour_tab, "Behaviour")
        self.tab_widget.addTab(self.audio_tab, "Audio")

    def button_box_accepted(self):
        self.mainwindow.options.save_user_defaults(timer_interval=self.behaviour_scrolling_text_speed,
                                                   play_button_behaviour=self.behaviour_play_button,
                                                   playlist_autoplay=self.behaviour_playlist_autoplay,
                                                   output_device=self.audio_output_device)

        self.mainwindow.music_info_box.set_timers_interval()
        self.close()

    def button_box_rejected(self):
        self.close()
