from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel, QListWidget,\
    QListView, QAbstractItemView, QTreeView
from PyQt5.QtCore import Qt, QSize

import os.path

import files


# noinspection PyArgumentList
class FoldersManager(QWidget):
    def __init__(self, main_parent=None):
        super(FoldersManager, self).__init__()
        self.mainwindow = main_parent

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(50, 50, 350, 250)
        self.setMinimumSize(450, 350)
        self.setMaximumSize(450, 350)
        self.setFont(QFont("Consolas", 10))
        self.setWindowTitle("Folders Manager")
        self.setWindowIcon(QIcon(files.Images.HQPLAYER_LOGO))

        self.explanation_label = QLabel(self)
        self.explanation_label.setGeometry(14, 20, 250, 16)
        self.explanation_label.setToolTip("Music folders used for the playlist.")
        self.explanation_label.setText("Music folders used for the playlist.")

        self.add_button = QPushButton(self)
        self.add_button.setGeometry(405, 60, 25, 25)
        self.add_button.setToolTip("Add folder")
        self.add_button.setIcon(QIcon(files.Images.ADD))
        self.add_button.setIconSize(QSize(25, 25))
        self.add_button.setFocusPolicy(Qt.ClickFocus)

        self.remove_button = QPushButton(self)
        self.remove_button.setGeometry(405, 90, 25, 25)
        self.remove_button.setToolTip("Remove folder")
        self.remove_button.setIcon(QIcon(files.Images.REMOVE))
        self.remove_button.setIconSize(QSize(25, 25))
        self.remove_button.setFocusPolicy(Qt.ClickFocus)

        self.folder_list = QListWidget(self)
        self.folder_list.setGeometry(10, 40, 373, 300)
        self.folder_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.folder_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.folder_list.setEditTriggers(QListWidget.SelectedClicked)
        self.folder_list.setDefaultDropAction(Qt.IgnoreAction)

        self.add_button.released.connect(self.ab_released)
        self.add_button.clicked.connect(self.ab_clicked)
        self.remove_button.released.connect(self.rm_released)
        self.remove_button.clicked.connect(self.rm_clicked)

    def remove_sel(self):
        list_items = self.folder_list.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.folder_list.takeItem(self.folder_list.row(item))

    def refresh_list(self):
        self.folder_list.clear()
        if self.mainwindow.options.user_music_folders is not None:
            for folder in self.mainwindow.options.user_music_folders:
                self.folder_list.addItem(folder)
        self.folder_list.sortItems()

    def get_selected_item(self):
        return (self.folder_list.selectedItems()[0]).text()

    def ab_released(self):
        self.add_button.clearFocus()

    def rm_released(self):
        self.remove_button.clearFocus()

    def ab_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setDirectory(self.mainwindow.options.get_default_last_folder_opened())
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(QListView, 'listView')

        # to make it possible to select multiple directories:
        if file_view:
            file_view.setSelectionMode(QAbstractItemView.MultiSelection)
        f_tree_view = file_dialog.findChild(QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QAbstractItemView.MultiSelection)

        if file_dialog.exec():
            folders = file_dialog.selectedFiles()

            if len(folders) != 0:
                for folder in folders:
                    parent_folder = os.path.dirname(r"{}".format(folder))
                    self.mainwindow.options.save_user_defaults(music_folder=folder, last_folder_opened=parent_folder)
                    self.folder_list.addItem(folder)
                    self.folder_list.sortItems()

        # folder = QFileDialog.getExistingDirectory(self, "Add Folder(s)",
        #                                           self.mainwindow.options.get_default_last_folder_opened(),
        #                                           QFileDialog.ShowDirsOnly)

    def rm_clicked(self):
        if len(self.folder_list.selectedItems()) != 0:
            self.mainwindow.options.delete_music_folder(self.get_selected_item())
            self.remove_sel()
