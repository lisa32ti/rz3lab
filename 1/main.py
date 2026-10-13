import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox


class StatsApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "task1.ui"), self)

        self.numbers = []
        self.btnLoad.clicked.connect(self.load_file)
        self.btnSave.clicked.connect(self.save_file)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Text files (*.txt);;All files (*)"
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot open file:\n{e}")
            return

        tokens = content.split()
        if not tokens:
            QMessageBox.warning(self, "Error", "File is empty")
            return

        numbers = []
        for t in tokens:
            try:
                numbers.append(int(t))
            except ValueError:
                QMessageBox.warning(self, "Error",
                                    f"File contains non-number: '{t}'")
                return

        self.numbers = numbers
        self.update_labels()

    def update_labels(self):
        if not self.numbers:
            return
        mx = max(self.numbers)
        mn = min(self.numbers)
        avg = sum(self.numbers) / len(self.numbers)

        self.labelMax.setText(f"Max: {mx}")
        self.labelMin.setText(f"Min: {mn}")
        self.labelAvg.setText(f"Average: {avg:.3f}")

    def save_file(self):
        if not self.numbers:
            QMessageBox.warning(self, "Error", "Load a file first")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save file", "result.txt", "Text files (*.txt)"
        )
        if not path:
            return

        mx = max(self.numbers)
        mn = min(self.numbers)
        avg = sum(self.numbers) / len(self.numbers)

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"Max: {mx}\n")
                f.write(f"Min: {mn}\n")
                f.write(f"Average: {avg:.3f}\n")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot save:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = StatsApp()
    w.show()
    sys.exit(app.exec_())