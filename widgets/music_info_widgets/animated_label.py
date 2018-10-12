from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import QTimer

import util


# noinspection PyUnresolvedReferences,PyArgumentList
class AnimatedLabel(QWidget):
    def __init__(self, parent=None, y=0, name="None", animate_option=True):
        super(AnimatedLabel, self).__init__(parent)
        self.setGeometry(10, y, 218, 13)

        self.original_text = ""
        self.original_text_pixel_width = 0
        self.animate_option = animate_option

        self.label_name = QLabel(self)
        self.label_name.setGeometry(0, 0, 48, 13)
        self.label_name.setText(name)

        self.label = QLabel(self)
        self.label.setGeometry(54, 0, 170, 13)

        self.timer_interval_delay = 1500
        self.timer_interval = self.mainwindow.options.get_default_timer_interval()

        self.timer = QTimer()
        self.timer.setInterval(self.timer_interval)
        self.timer.timeout.connect(self.animate_label_text)

    @property
    def mainwindow(self):
        return util.get_upper_parentwidget(self, 3)

    def animate_label_text(self):
        """Animates the text by moving the text to the left once"""
        if self.animate_option and self.original_text_pixel_width > 160:
            self.label.setText((self.label.text()[1:] + self.label.text()[:1]))

            if "{}      ".format(self.original_text) == self.label.text():
                self.timer.setInterval(self.timer_interval_delay)
            else:
                self.timer.setInterval(self.timer_interval)

    def set_label_text(self, text):
        self.original_text = text
        self.label.setText(text)
        self.setToolTip(text)

        self.original_text_pixel_width = self.label.fontMetrics().boundingRect(self.label.text()).width()
        if self.original_text_pixel_width > 160:
            self.label.setText("{}      ".format(text))

    def reset_label_text(self):
        self.label.setText("")
        self.setToolTip("")
