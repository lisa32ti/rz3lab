import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QTransform
from PyQt5.QtCore import Qt, QTimer


class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "task3.ui"), self)

        self.original = None
        self.current = None

        self.btnChannelR.clicked.connect(lambda: self.keep_channel("R"))
        self.btnChannelG.clicked.connect(lambda: self.keep_channel("G"))
        self.btnChannelB.clicked.connect(lambda: self.keep_channel("B"))
        self.btnRotateLeft.clicked.connect(lambda: self.rotate(-90))
        self.btnRotateRight.clicked.connect(lambda: self.rotate(90))

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

        img = img.convertToFormat(QImage.Format_ARGB32)

        if img.width() > 400 or img.height() > 400:
            img = img.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        side = min(img.width(), img.height())
        x = (img.width() - side) // 2
        y = (img.height() - side) // 2
        img = img.copy(x, y, side, side)

        self.original = img
        self.current = img.copy()
        self.update_view()

    def update_view(self):
        if self.current is None:
            return
        pix = QPixmap.fromImage(self.current)
        self.imageLabel.setPixmap(pix)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setFixedSize(300, 300)

    def keep_channel(self, channel):
        if self.original is None:
            return

        img = self.original.convertToFormat(QImage.Format_ARGB32)
        w = img.width()
        h = img.height()

        ptr = img.bits()
        ptr.setsize(img.byteCount())
        arr = bytearray(ptr.asstring())

        for i in range(0, len(arr), 4):
            if channel == "R":
                arr[i] = 0
                arr[i + 1] = 0
            elif channel == "G":
                arr[i] = 0
                arr[i + 2] = 0
            else:
                arr[i + 1] = 0
                arr[i + 2] = 0

        result = QImage(bytes(arr), w, h, img.bytesPerLine(), QImage.Format_ARGB32)
        self.current = result.copy()
        self.update_view()

    def rotate(self, angle):
        if self.current is None:
            return
        pix = QPixmap.fromImage(self.current)
        rotated = pix.transformed(QTransform().rotate(angle))
        self.current = rotated.toImage()
        self.update_view()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageEditor()
    w.show()
    sys.exit(app.exec_())