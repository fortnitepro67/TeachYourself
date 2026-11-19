"""App entry point: tabs for Tuner and Theory."""
import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QComboBox, QTabWidget
from PySide6.QtCore import Qt, Signal, QObject

sys.path.append(".")
from src.audio.input_stream import MicPitchListener, list_input_devices, default_input_device
from src.audio.pitch_detection import nearest_target
from src.content.guitar_notes import STANDARD_TUNING_FREQS
from src.ui.theory_screen import TheoryScreen


class NoteSignal(QObject):
    updated = Signal(object, object)  # freq, note


class TunerTab(QWidget):
    def __init__(self):
        super().__init__()

        self.device_box = QComboBox()
        self.devices = list_input_devices()
        current_default = default_input_device()
        for index, name in self.devices:
            self.device_box.addItem(name, userData=index)
        default_pos = next((i for i, (idx, _) in enumerate(self.devices) if idx == current_default), 0)
        self.device_box.setCurrentIndex(default_pos)
        self.device_box.currentIndexChanged.connect(self._on_device_changed)

        self.label = QLabel("Spiel eine Note...")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 48px;")

        self.detail_label = QLabel("")
        self.detail_label.setAlignment(Qt.AlignCenter)
        self.detail_label.setStyleSheet("font-size: 20px;")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Mikrofon:"))
        layout.addWidget(self.device_box)
        layout.addWidget(self.label)
        layout.addWidget(self.detail_label)
        self.setLayout(layout)

        self.signal = NoteSignal()
        self.signal.updated.connect(self._on_update)
        self.listener = None
        self._start_listener(self.device_box.currentData())

    def _start_listener(self, device_index):
        if self.listener:
            self.listener.stop()
        self.listener = MicPitchListener(self._on_note, device=device_index)
        self.listener.start()

    def _on_device_changed(self, _index):
        self._start_listener(self.device_box.currentData())

    def _on_note(self, freq, note):
        self.signal.updated.emit(freq, note)

    def _on_update(self, freq, note):
        if not note:
            self.label.setText("Spiel eine Note...")
            self.detail_label.setText("")
            return

        name, target_freq, cents = nearest_target(freq, STANDARD_TUNING_FREQS)
        self.label.setText(f"{name}  ({freq:.1f} Hz)")
        if abs(cents) < 5:
            self.detail_label.setText("Perfekt gestimmt")
            self.detail_label.setStyleSheet("font-size: 20px; color: green;")
        elif cents < 0:
            self.detail_label.setText(f"zu tief ({cents:.0f} Cent) - hoeher drehen")
            self.detail_label.setStyleSheet("font-size: 20px; color: orange;")
        else:
            self.detail_label.setText(f"zu hoch (+{cents:.0f} Cent) - tiefer drehen")
            self.detail_label.setStyleSheet("font-size: 20px; color: orange;")

    def stop(self):
        if self.listener:
            self.listener.stop()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TeachYourself")
        self.resize(460, 340)

        self.tuner_tab = TunerTab()
        tabs = QTabWidget()
        tabs.addTab(self.tuner_tab, "Tuner")
        tabs.addTab(TheoryScreen(), "Theorie")

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)

    def closeEvent(self, event):
        self.tuner_tab.stop()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
