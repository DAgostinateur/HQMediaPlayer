from PyQt5.QtWidgets import QLabel, QWidget


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

    def animate_label_text(self):
        """Animates the text by moving the text to the left once"""
        if self.animate_option and self.original_text_pixel_width > 160:
            self.label.setText((self.label.text()[1:] + self.label.text()[:1]))

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
