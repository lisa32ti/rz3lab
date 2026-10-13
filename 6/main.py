import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QColorDialog
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt


class Smile(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "task6.ui"), self)

        self.smile_color = QColor(255, 220, 0)
        self.scale = 100

        self.sliderScale.setRange(10, 200)
        self.sliderScale.setValue(100)
        self.sliderScale.valueChanged.connect(self.change_scale)

        self.btnColor.clicked.connect(self.choose_color)

        self.update_label()

    def choose_color(self):
        color = QColorDialog.getColor(
            self.smile_color, self, "Выберите цвет смайлика"
        )
        if color.isValid():
            self.smile_color = color
            self.update()

    def change_scale(self, value):
        self.scale = value
        self.update_label()
        self.update()

    def update_label(self):
        self.labelInfo.setText(f"Scale: {self.scale}%")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        base = min(self.width(), self.height()) // 3
        radius = int(base * self.scale / 100)

        cx = self.width() // 2
        cy = (self.height() - 80) // 2

        painter.setBrush(QBrush(self.smile_color))
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)

        eye_r = max(2, radius // 8)
        painter.setBrush(QBrush(Qt.black))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - radius // 2 - eye_r,
                            cy - radius // 3 - eye_r,
                            eye_r * 2, eye_r * 2)
        painter.drawEllipse(cx + radius // 2 - eye_r,
                            cy - radius // 3 - eye_r,
                            eye_r * 2, eye_r * 2)

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.black, max(2, radius // 20)))
        smile_w = radius
        smile_h = radius // 2
        painter.drawArc(
            cx - smile_w // 2,
            cy - smile_h // 2,
            smile_w,
            smile_h,
            180 * 16,
            180 * 16
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Smile()
    w.show()
    sys.exit(app.exec_())