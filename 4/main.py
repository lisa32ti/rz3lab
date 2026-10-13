import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer


class TransparentImage(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "task4.ui"), self)

        self.original = None

        self.imageLabel.setFixedSize(400, 400)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setStyleSheet("border: 1px solid gray;")

        self.sliderAlpha.setRange(0, 100)
        self.sliderAlpha.setValue(100)
        self.sliderAlpha.valueChanged.connect(self.update_image)

        self.setFixedSize(500, 520)

        QTimer.singleShot(200, self.load_image)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open image", "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not path:
            return

        img = QImage(path)
        if img.isNull():
            QMessageBox.critical(self, "Error", "Cannot load image")
            return

        img = img.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.original = img.convertToFormat(QImage.Format_ARGB32)
        self.update_image()

    def update_image(self):
        if self.original is None:
            return

        alpha = self.sliderAlpha.value()
        self.labelValue.setText(f"Alpha: {alpha}%")

        img = self.original
        w = img.width()
        h = img.height()

        ptr = img.bits()
        ptr.setsize(img.byteCount())
        arr = bytearray(ptr.asstring())

        for i in range(3, len(arr), 4):
            arr[i] = int(arr[i] * alpha / 100)

        result = QImage(bytes(arr), w, h, img.bytesPerLine(), QImage.Format_ARGB32)
        pix = QPixmap.fromImage(result)

        self.imageLabel.setPixmap(pix)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TransparentImage()
    w.show()
    sys.exit(app.exec_())