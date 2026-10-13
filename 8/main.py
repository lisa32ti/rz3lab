import sys
import os
import math
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QTimer


class LSystem(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "task8.ui"), self)

        self.name = ""
        self.axiom = ""
        self.rules = {}
        self.angle_step = 72
        self.iterations = 0

        self.sliderIter.setRange(0, 5)
        self.sliderIter.setValue(0)
        self.sliderIter.valueChanged.connect(self.change_iter)

        QTimer.singleShot(200, self.load_definition)

    def load_definition(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open L-System", "", "Text files (*.txt);;All files (*)"
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        if len(lines) < 4:
            QMessageBox.warning(self, "Error", "File must have at least 4 lines")
            return

        self.name = lines[0]

        try:
            n = int(lines[1])
        except ValueError:
            QMessageBox.warning(self, "Error", "Second line must be a number")
            return

        self.angle_step = 360 / n
        self.axiom = lines[2]

        self.rules = {}
        for line in lines[3:]:
            if "=" in line:
                left, right = line.split("=", 1)
                self.rules[left.strip()] = right.strip()

        self.setWindowTitle(f"L-System: {self.name}")
        self.iterations = 0
        self.sliderIter.setValue(0)
        self.update()

    def change_iter(self, value):
        self.iterations = value
        self.labelInfo.setText(f"Iteration: {value}")
        self.update()

    def generate(self, iterations):
        s = self.axiom
        for _ in range(iterations):
            s = "".join(self.rules.get(ch, ch) for ch in s)
        return s

    def paintEvent(self, event):
        if not self.axiom:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 1))

        s = self.generate(self.iterations)

        x = self.width() // 2
        y = self.height() // 4
        angle = 0

        base = min(self.width(), self.height()) / 2
        step = max(1, base / (3 ** self.iterations))

        stack = []

        for ch in s:
            if ch == "F":
                rad = math.radians(angle)
                nx = x + step * math.cos(rad)
                ny = y + step * math.sin(rad)
                painter.drawLine(int(x), int(y), int(nx), int(ny))
                x, y = nx, ny
            elif ch == "+":
                angle += self.angle_step
            elif ch == "-":
                angle -= self.angle_step
            elif ch == "[":
                stack.append((x, y, angle))
            elif ch == "]":
                if stack:
                    x, y, angle = stack.pop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = LSystem()
    w.show()
    sys.exit(app.exec_())