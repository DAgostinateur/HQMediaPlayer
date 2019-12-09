from PyQt5.QtWidgets import QDialogButtonBox, QDialog, QTabWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QAudio, QAudioDeviceInfo

import files
import hqmediaplayer
import util
from widgets.option_dialog_widgets import behaviour_tab, audio_tab


# noinspection PyUnresolvedReferences,PyArgumentList,PyAttributeOutsideInit
class OptionsDialog(QDialog):
    behaviour_play_button_restart = 1
    behaviour_play_button_nothing = 2

    behaviour_playlist_autoplay_start = 1
    behaviour_playlist_autoplay_nothing = 2

    def __init__(self, main_parent: hqmediaplayer.HQMediaPlayer = None):
        super(OptionsDialog, self).__init__()
        self.mainwindow = main_parent

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(50, 50, 400, 265)
        self.setMinimumSize(400, 265)
        self.setFont(QFont("Consolas", 10))
        self.setWindowTitle("Options")
        self.setWindowIcon(QIcon(files.Images.HQPLAYER_LOGO))
        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))

        self.behaviour_play_button = self.mainwindow.options.get_default_play_button()
        self.behaviour_playlist_autoplay = self.mainwindow.options.get_default_playlist_autoplay()
        self.behaviour_scrolling_text_speed = self.mainwindow.options.get_default_timer_interval()
        self.audio_output_device = self.mainwindow.options.get_default_output_device()

        self.behaviour_tab = behaviour_tab.BehaviourTab()
        self.audio_tab = audio_tab.AudioTab()

        self.create_tabs()

        self.button_box = QDialogButtonBox(self)
        self.button_box.setGeometry(20, 220, 360, 32)
        self.button_box.setStandardButtons(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        self.button_box.accepted.connect(self.button_box_accepted)
        self.button_box.rejected.connect(self.button_box_rejected)

    def update_info_choices(self):
        if self.behaviour_play_button == self.behaviour_play_button_restart:
            self.behaviour_tab.option_play_button.radio_restart.setChecked(True)
        else:
            self.behaviour_tab.option_play_button.radio_nothing.setChecked(True)

        if self.behaviour_playlist_autoplay == self.behaviour_playlist_autoplay_start:
            self.behaviour_tab.option_playlist_autoplay.radio_autoplay.setChecked(True)
        else:
            self.behaviour_tab.option_playlist_autoplay.radio_no_autoplay.setChecked(True)

        self.behaviour_tab.option_scrolling_text.spin_millisecond.setValue(self.mainwindow.options.get_default_option(
            self.mainwindow.options.default_user_timer_interval,
            self.mainwindow.options.default_app_timer_interval))

        self.audio_tab.option_output_device.label_selected_device.setToolTip(
            self.mainwindow.options.get_default_output_device())
        self.audio_tab.option_output_device.label_selected_device.setText(
            "Current: {}".format(self.mainwindow.options.get_default_output_device()))

        self.audio_tab.option_output_device.combo_box_selected_device.clear()
        for device in QAudioDeviceInfo.availableDevices(QAudio.AudioOutput):
            self.audio_tab.option_output_device.combo_box_selected_device.addItem(device.deviceName())
            if self.audio_tab.option_output_device.combo_box_selected_device.count() == len(
                    QAudioDeviceInfo.availableDevices(QAudio.AudioOutput)) / 2:
                self.audio_tab.option_output_device.combo_box_selected_device.addItem(
                    self.mainwindow.options.default_app_output_device)
                break
        for text, index in util.get_all_combo_box_items(self.audio_tab.option_output_device.combo_box_selected_device):
            if text == self.mainwindow.options.get_default_output_device():
                self.audio_tab.option_output_device.combo_box_selected_device.setCurrentIndex(index)

    def create_tabs(self):
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(20, 10, 360, 200)
        self.tab_widget.resize(360, 200)
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
