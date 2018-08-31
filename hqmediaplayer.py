import ctypes
import sys

import pypresence.client
import pypresence.exceptions
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QKeyEvent, QCloseEvent, QIcon, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QAudioDeviceInfo, QAudio
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog

import audio
import files
import options_dialog
import util
from widgets import (music_control_box, music_info_box, full_menubar,
                     embedded_console, folders_manager)


# TODO:
# Songs playing longer than they should? Or is the duration slider wrong?
#   When moving the duration slider, when the mp3 file's length has been modified, it will
#   not change value correctly.
#
# Look into "directshowplayerservice::dorender: unresolved error code 0x80040266"
#   It's a .mp3 metadata problem. Versions of ID3 cause the issues.
#   Found the bug:
#       https://bugreports.qt.io/browse/QTBUG-42286
#   Fix:
#       Change ID3 Tags to ID3v2.3 ISO-8859-1
#       ID#v2.4, ID3v2.3 UTF-16 and UTF-8 were causing problems
#
# Being able to change output device
# QtxGlobalShortcuts, look into that
# About Section
# Add info on README.md


# Fixes the TaskBar Icon bug
# https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("dagostinateur_woh.hqmediaplayer")


# noinspection PyCallByClass,PyArgumentList,PyUnresolvedReferences
class HQMediaPlayer(QMainWindow):
    # Is this supposed to be hidden?
    # There's no mention in pypresence or Discord documents to hide the application client id.
    drpc_client_id = '434146683245297684'

    def __init__(self, parent=None):
        super(HQMediaPlayer, self).__init__(parent)
        self.key_list = []
        self.first_release = False

        self.setMinimumSize(702, 474)
        self.setFont(QFont("Consolas"))
        self.setWindowTitle("HQMediaPlayer")
        self.setIconSize(QSize(32, 32))
        self.setWindowIcon(QIcon(files.Images.HQPLAYER_LOGO))

        self.centralwidget = QWidget(self)
        self.centralwidget.setGeometry(0, 21, 702, 433)

        # drpc = Discord Rich Presence
        # The id that goes with it is the discord client id of the application
        self.drpc = None
        self.drpc_enabled = False

        self.options = options_dialog.Options()
        self.song = audio.WSong()
        self.playlist = audio.WPlaylist(self)
        self.dbg_console = embedded_console.EmbeddedConsole()
        self.music_control_box = music_control_box.MusicControlBox(self.centralwidget)
        self.music_info_box = music_info_box.MusicInfoBox(self.centralwidget)
        self.options_dialog = options_dialog.OptionsDialog(self)
        self.fol_man = folders_manager.FoldersManager(self)

        full_menubar.create_full_menubar(self)
        self.restart_drpc()

        # all_devices = ""
        # test = QAudioDeviceInfo.availableDevices(QAudio.AudioOutput)[0]
        #
        # for d in QAudioDeviceInfo.availableDevices(QAudio.AudioOutput):
        #
        #     all_devices += "{}\n".format(d.deviceName())
        #     print(d.supportedCodecs())
        # else:
        #     print(all_devices)

    def debug_console_action_triggered(self):
        self.dbg_console.show()

    def set_drpc_activity(self, state):
        self.restart_drpc()
        if self.drpc_enabled:
            try:
                if self.song.has_song():
                    self.drpc.set_activity(large_image="app_logo",
                                           state="Player {}".format(state),
                                           details="Listening to '{}'".format(self.song.get_info(audio.WSong.TITLE)))
                else:
                    self.drpc.set_activity(large_image="app_logo",
                                           state="Player {}".format(state),
                                           details="Listening to 'N/A'")
            except pypresence.exceptions.InvalidID:
                self.drpc_enabled = False
                self.drpc.close()

    def restart_drpc(self):
        if not self.drpc_enabled:
            try:
                self.drpc_enabled = True
                self.drpc = pypresence.client.Client(self.drpc_client_id)
                self.drpc.start()
                self.music_control_box.player.state_changed(self.music_control_box.player.state())
            except pypresence.exceptions.InvalidPipe:
                self.drpc_enabled = False

    def open_about(self):
        pass

    def start_playlist(self):
        self.playlist.clear()
        self.music_control_box.player.has_playlist = False
        if len(self.options.user_music_folders) == 0:
            return

        self.playlist.set_playlist_files()
        self.playlist.shuffle()
        self.music_control_box.player.setPlaylist(self.playlist)
        self.song.set_song(self.playlist.get_current_song())

        self.music_control_box.player.has_playlist = True

        self.music_control_box.stop_button.sb_clicked()
        self.music_control_box.play_button.plb_clicked()

    def open_file(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, "Open File", "/", "MP3 (*.mp3)")
        if ".mp3" in file_type:
            self.playlist.clear()
            self.music_control_box.player.has_playlist = False
            self.song.set_song(file_name)
            self.music_control_box.player.setMedia(self.song.content)
            self.music_control_box.stop_button.sb_clicked()
            self.music_control_box.play_button.plb_clicked()

    def open_folders_manager(self):
        self.fol_man.refresh_list()
        self.fol_man.show()

    def open_options_menu(self):
        self.options_dialog.update_info_choices()
        self.options_dialog.show()

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
        if (util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Home]) or
                util.check_keys(key_list, [Qt.Key_MediaTogglePlayPause])):
            if self.music_control_box.player.state() == QMediaPlayer.PlayingState:
                self.music_control_box.pause_button.pb_clicked()
            elif self.music_control_box.player.state() == QMediaPlayer.PausedState or \
                    self.music_control_box.player.state() == QMediaPlayer.StoppedState:
                self.music_control_box.play_button.plb_clicked()

        elif util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Up]):
            self.music_control_box.volume_slider.increase_volume(5)
        elif util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Down]):
            self.music_control_box.volume_slider.decrease_volume(5)
        elif util.check_keys(key_list, [Qt.Key_MediaStop]):
            self.music_control_box.stop_button.sb_clicked()
        # elif util.check_keys(key_list, [Qt.Key_MediaPlay]):
        #     self.music_control_box.play_button.plb_clicked()
        # elif util.check_keys(key_list, [Qt.Key_MediaPause]):
        #     self.music_control_box.pause_button.pb_clicked()
        elif util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_H, Qt.Key_Q]):
            self.music_control_box.play_button.toggle_icon_status()
        elif util.check_keys(key_list, [Qt.Key_MediaNext]):
            pass
        elif util.check_keys(key_list, [Qt.Key_MediaPrevious]):
            pass

        # self.dbg_console.write(key_list)

        if any(key_list.count(x) > 1 for x in key_list):
            del key_list[:]

    def closeEvent(self, event: QCloseEvent):
        if self.drpc_enabled:
            self.drpc.close()

        self.options.save_user_defaults(self.music_control_box.volume_slider.value(), None, None, None)
        self.dbg_console.close()
        self.options_dialog.close()
        self.fol_man.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    media_player = HQMediaPlayer()
    media_player.show()
    sys.exit(app.exec_())
