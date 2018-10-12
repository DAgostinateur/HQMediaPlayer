from PyQt5.QtMultimedia import QAudioDeviceInfo

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
