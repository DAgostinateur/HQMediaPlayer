from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget
from PyQt5.Qt import Qt


# noinspection PyUnresolvedReferences,PyArgumentList
class AnimatedLabel(QWidget):
    def __init__(self, parent=None, y=0, label_name="None", animate_option=True):
        super(AnimatedLabel, self).__init__(parent)
        self.setGeometry(10, y, 218, 13)

        self.original_text = ""
        self.original_text_pixel_width = 0
        self.animate_option = animate_option

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 48, 13)
        self.label.setText(label_name)

        self.line_edit = QLineEdit(self)
        self.line_edit.setGeometry(54, 0, 170, 13)
        self.line_edit.setCursor(Qt.IBeamCursor)
        self.line_edit.setStyleSheet("QLineEdit{background-color: #F0F0F0;}")
        self.line_edit.setFrame(False)
        self.line_edit.setReadOnly(True)

    def animate_cursor(self):
        if self.animate_option and self.original_text_pixel_width > 170:
            self.line_edit.setText((self.line_edit.text()[1:] + self.line_edit.text()[:1]))

    def set_line_edit_text(self, text):
        self.original_text = text

        self.line_edit.setText(text)
        self.line_edit.setToolTip(text)
        self.line_edit.setCursorPosition(0)

        self.original_text_pixel_width = self.line_edit.fontMetrics().boundingRect(self.line_edit.text()).width()
        if self.original_text_pixel_width > 170:
            self.line_edit.setText("{}      ".format(text))

    def reset_line_edit_text(self):
        self.line_edit.setText("")
        self.line_edit.setToolTip("")
