from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtGui import QFont


def create_full_menubar(hqmediaplayer):
    debug_console_action = QAction(hqmediaplayer)
    debug_console_action.setText("Debug Console")
    debug_console_action.setIconText("Debug Console")
    debug_console_action.setFont(QFont("Consolas", 10))
    debug_console_action.triggered.connect(hqmediaplayer.debug_console_action_triggered)

    start_playlist_action = QAction(hqmediaplayer)
    start_playlist_action.setText("Start Playlist")
    start_playlist_action.setIconText("Start Playlist")
    start_playlist_action.setFont(QFont("Consolas", 10))
    start_playlist_action.setShortcut("Ctrl+P")
    start_playlist_action.triggered.connect(hqmediaplayer.start_playlist)

    open_file_action = QAction(hqmediaplayer)
    open_file_action.setText("Open File")
    open_file_action.setIconText("Open File")
    open_file_action.setFont(QFont("Consolas", 10))
    open_file_action.setShortcut("Ctrl+O")
    open_file_action.triggered.connect(hqmediaplayer.open_file)

    open_folder_action = QAction(hqmediaplayer)
    open_folder_action.setText("Open from Folder")
    open_folder_action.setIconText("Open from Folder")
    open_folder_action.setFont(QFont("Consolas", 10))
    open_folder_action.triggered.connect(hqmediaplayer.open_folder)

    folder_manager_action = QAction(hqmediaplayer)
    folder_manager_action.setText("Folders Manager")
    folder_manager_action.setIconText("Folders Manager")
    folder_manager_action.setFont(QFont("Consolas", 10))
    folder_manager_action.triggered.connect(hqmediaplayer.open_folders_manager)

    options_action = QAction(hqmediaplayer)
    options_action.setText("Options")
    options_action.setIconText("Options")
    options_action.setFont(QFont("Consolas", 10))
    options_action.triggered.connect(hqmediaplayer.open_options_menu)

    restart_drpc_action = QAction(hqmediaplayer)
    restart_drpc_action.setText("Restart Discord rich presence")
    restart_drpc_action.setIconText("Restart Discord rich presence")
    restart_drpc_action.setFont(QFont("Consolas", 10))
    restart_drpc_action.triggered.connect(hqmediaplayer.restart_drpc)

    about_action = QAction(hqmediaplayer)
    about_action.setText("About")
    about_action.setIconText("About")
    about_action.setFont(QFont("Consolas", 10))
    about_action.triggered.connect(hqmediaplayer.open_about)

    file_menu = QMenu(hqmediaplayer)
    file_menu.setTitle("File")
    file_menu.setFont(QFont("Consolas", 10))
    file_menu.addAction(start_playlist_action)
    file_menu.addAction(open_file_action)
    file_menu.addAction(open_folder_action)
    file_menu.addAction(folder_manager_action)
    file_menu.addAction(options_action)

    help_menu = QMenu(hqmediaplayer)
    help_menu.setTitle("Help")
    help_menu.setFont(QFont("Consolas", 10))
    help_menu.addAction(debug_console_action)
    help_menu.addAction(restart_drpc_action)
    help_menu.addAction(about_action)

    menubar = hqmediaplayer.menuBar()
    menubar.addMenu(file_menu)
    menubar.addMenu(help_menu)
