import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "task2.ui"), self)

        self.current_path = None
        self.actionOpen.triggered.connect(self.open_file)
        self.actionNew.triggered.connect(self.new_file)
        self.actionSave.triggered.connect(self.save_file)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open", "", "Text files (*.txt); All files (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.textBrowser.setPlainText(f.read())
            self.current_path = path
            self.setWindowTitle(f"Editor — {os.path.basename(path)}")
        except Exception as e:
            QMessageBox.critical(self, "error", str(e))

    def new_file(self):
        self.textBrowser.clear()
        self.current_path = None
        self.setWindowTitle("Editor — new file")

    def save_file(self):
        if self.current_path is None:
            path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить", "new.txt", "Text files (*.txt)"
            )
            if not path:
                return
        else:
            path = self.current_path

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.textBrowser.toPlainText())
            self.current_path = path
            self.setWindowTitle(f"Editor — {os.path.basename(path)}")
        except Exception as e:
            QMessageBox.critical(self, "error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Editor()
    w.show()
    sys.exit(app.exec_())