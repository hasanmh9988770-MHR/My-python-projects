from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
    QFileDialog, QMessageBox, QLineEdit
)
from PySide6.QtCore import Qt


class StegoApp(QWidget):
    def __init__(self, pipeline):
        super().__init__()
        self.pipeline = pipeline

        self.setWindowTitle("Stego System ULTRA PRO")
        self.setFixedSize(450, 350)

        self.setStyleSheet("""
            QWidget {
                background-color: #0f0f0f;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1f1f1f;
                border: 1px solid #333;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
            QLineEdit {
                background-color: #1a1a1a;
                border: 1px solid #333;
                padding: 6px;
            }
        """)

        layout = QVBoxLayout()

        self.title = QLabel("STEGO SYSTEM ULTRA PRO MAX")
        self.title.setAlignment(Qt.AlignCenter)

        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Enter message")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter password")
        self.pass_input.setEchoMode(QLineEdit.Password)

        btn_encode = QPushButton("ENCODE MESSAGE")
        btn_decode = QPushButton("DECODE MESSAGE")

        btn_encode.clicked.connect(self.encode)
        btn_decode.clicked.connect(self.decode)

        layout.addWidget(self.title)
        layout.addWidget(self.msg_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(btn_encode)
        layout.addWidget(btn_decode)

        self.setLayout(layout)

        self.file_path = None

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image")
        return path

    def encode(self):
        file = self.select_file()
        if not file:
            return

        try:
            out = self.pipeline.encode(
                self.msg_input.text(),
                self.pass_input.text(),
                file
            )
            QMessageBox.information(self, "SUCCESS", f"Saved:\n{out}")
        except Exception as e:
            QMessageBox.critical(self, "ERROR", str(e))

    def decode(self):
        file = self.select_file()
        if not file:
            return

        try:
            msg = self.pipeline.decode(
                file,
                self.pass_input.text()
            )

            if msg:
                QMessageBox.information(self, "MESSAGE", msg)
            else:
                QMessageBox.warning(self, "FAILED", "No data found")

        except Exception as e:
            QMessageBox.critical(self, "ERROR", str(e))