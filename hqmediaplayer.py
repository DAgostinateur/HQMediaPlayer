import ctypes
import sys

import pypresence.client
import pypresence.exceptions
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QKeyEvent, QCloseEvent, QIcon, QFont
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog

import audio
import files
import options_dialog
import util
from widgets import (music_control_box, music_info_box, full_menubar,
                     debug_console, folders_manager)


# TODO:
# A way to see all the songs in the playlist
# QtxGlobalShortcuts, look into that
# About Section
# More Options
# Add info on README.md
#
#
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
# There's a bug with the fix I added to the double multimedia key input bug. It sometimes doesnt work.
#   The alt key would randomly be pressed, even though it's not, and that would mess up the multimedia key.
#   Now it doesnt, but pressing multiple multimedia key at the same time causes them to not work afterwards, until
#   a non multimedia key gets pressed.
#
# Being able to change output device
#   PyQt5 doesnt have the code required to change audio device output, it's in Qt5 though.
#   Maybe using other packages would make this possible, but WMediaPlayer and WPlaylist would have to be rewritten.


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

        self.multimedia_key_pressed = False
        self.multimedia_key = None

        self.setMinimumSize(702, 474)
        self.setMaximumSize(702, 474)
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
        self.debug_console = debug_console.EmbeddedConsole()
        self.music_control_box = music_control_box.MusicControlBox(self.centralwidget)
        self.music_info_box = music_info_box.MusicInfoBox(self.centralwidget)
        self.options_dialog = options_dialog.OptionsDialog(self)
        self.fol_man = folders_manager.FoldersManager(self)

        full_menubar.create_full_menubar(self)
        self.restart_drpc()

    def debug_console_action_triggered(self):
        self.debug_console.show()

    def set_drpc_activity(self, player_state: str):
        self.restart_drpc()
        if self.drpc_enabled:
            try:
                if self.song.has_song():
                    self.drpc.set_activity(state="Artist: {}".format(self.song.get_info(audio.WSong.ARTIST)),
                                           details="Listening to '{}'".format(self.song.get_info(audio.WSong.TITLE)),
                                           large_image="app_logo",
                                           small_image=player_state,
                                           small_text="Player {}".format(player_state.capitalize()))
                else:
                    self.drpc.set_activity(state="Artist: N/A",
                                           details="Listening to 'N/A'",
                                           large_image="app_logo",
                                           small_image=player_state,
                                           small_text="Player {}".format(player_state.capitalize()))
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

        if self.options.get_default_playlist_autoplay() == self.options_dialog.behaviour_playlist_autoplay_start:
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

    def rm_all_multimedia_keys(self):
        for key in self.key_list:
            if util.is_multimedia_key(key):
                self.key_list.remove(key)

    def keyPressEvent(self, event: QKeyEvent):
        # https://stackoverflow.com/questions/7176951/how-to-get-multiple-key-presses-in-single-event/10568233#10568233
        self.first_release = True
        self.key_list.append(int(event.key()))

    def keyReleaseEvent(self, event: QKeyEvent):
        if self.first_release:
            if util.is_multimedia_key(self.key_list[0]) and not self.multimedia_key_pressed:
                self.multimedia_key_pressed = not self.multimedia_key_pressed
                self.multimedia_key = self.key_list[0]
                self.debug_console.write("Multimedia Key Pressed: {}".format(str(self.key_list)))
            else:
                if self.multimedia_key is not None:
                    self.process_multi_keys([self.multimedia_key])

                    self.debug_console.write(
                        "Process Multimedia Key {} -- {}:".format(str(self.key_list), str(self.multimedia_key)))

                    # self.rm_all_multimedia_keys()
                    self.multimedia_key = None
                    self.multimedia_key_pressed = not self.multimedia_key_pressed
                else:
                    self.rm_all_multimedia_keys()
                    self.process_multi_keys(self.key_list)
                    self.debug_console.write("Process Any Keys: {}".format(str(self.key_list)))

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
            elif (self.music_control_box.player.state() == QMediaPlayer.PausedState or
                  self.music_control_box.player.state() == QMediaPlayer.StoppedState):
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
        elif util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.Key_H, Qt.Key_Q]):
            self.music_control_box.play_button.toggle_icon_status()
        elif (util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.RightArrow]) or
              util.check_keys(key_list, [Qt.Key_MediaNext])):
            self.music_control_box.next_button.nb_clicked()
        elif (util.check_keys(key_list, [Qt.Key_Control, Qt.Key_Alt, Qt.LeftArrow]) or
              util.check_keys(key_list, [Qt.Key_MediaPrevious])):
            self.music_control_box.previous_button.prb_clicked()

        # self.dbg_console.write(key_list)

        if any(key_list.count(x) > 1 for x in key_list):
            del key_list[:]

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton or event.button() == Qt.LeftButton:
            if self.music_control_box.volume_slider.volume_line_edit.isVisible():
                self.music_control_box.volume_slider.volume_line_edit.clearFocus()
                self.music_control_box.volume_slider.volume_line_edit.close()
        else:
            QMainWindow.mouseReleaseEvent(self, event)

    def closeEvent(self, event: QCloseEvent):
        if self.drpc_enabled:
            self.drpc.close()

        self.options.save_user_defaults(volume=self.music_control_box.volume_slider.value())
        self.debug_console.close()
        self.options_dialog.close()
        self.fol_man.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    media_player = HQMediaPlayer()
    media_player.show()
    sys.exit(app.exec_())
