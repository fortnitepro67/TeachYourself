"""MVP: live tuner window showing the detected note while playing."""
import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Signal, QObject

sys.path.append(".")
from src.audio.input_stream import MicPitchListener


class NoteSignal(QObject):
    updated = Signal(object, object)  # freq, note


class TunerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TeachYourself - Tuner")
        self.label = QLabel("Spiel eine Note...")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 48px;")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.resize(400, 200)

        self.signal = NoteSignal()
        self.signal.updated.connect(self._on_update)
        self.listener = MicPitchListener(self._on_note)
        self.listener.start()

    def _on_note(self, freq, note):
        self.signal.updated.emit(freq, note)

    def _on_update(self, freq, note):
        if note:
            self.label.setText(f"{note}  ({freq:.1f} Hz)")
        else:
            self.label.setText("Spiel eine Note...")

    def closeEvent(self, event):
        self.listener.stop()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = TunerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
