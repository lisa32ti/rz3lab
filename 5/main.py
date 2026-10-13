import sys
import os
import random
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog
from PyQt5.QtGui import QPixmap, QPainter, QColor


class FlagApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "task5.ui"), self)

        self.btnGenerate.clicked.connect(self.generate)

    def generate(self):
        count, ok = QInputDialog.getInt(
            self, "Количество цветов", "Введите число от 2 до 10:", 3, 2, 10, 1
        )
        if not ok:
            return

        width, height = 250, 180
        pix = QPixmap(width, height)
        painter = QPainter(pix)

        stripe_h = height / count
        for i in range(count):
            color = QColor(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            painter.fillRect(0, int(i * stripe_h),
                             width, int(stripe_h) + 1, color)

        painter.end()

        self.flagLabel.setPixmap(pix)
        self.flagLabel.setFixedSize(width, height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = FlagApp()
    w.show()
    sys.exit(app.exec_())