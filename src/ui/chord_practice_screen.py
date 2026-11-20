"""Chord practice tab: strum a chord, get per-string feedback."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton
from PySide6.QtCore import Qt, QThread, Signal

from src.content.chords import CHORD_SHAPES, STRING_NAMES, expected_frequencies
from src.audio.chord_detection import analyze_chord, chord_match_score
from src.audio.input_stream import record_clip
from src.ui.chord_diagram import ChordDiagramWidget

LISTEN_SECONDS = 1.5


class _ListenWorker(QThread):
    done = Signal(list)  # list[bool | None], one per string

    def __init__(self, expected_freqs, device):
        super().__init__()
        self.expected_freqs = expected_freqs
        self.device = device

    def run(self):
        samples, sample_rate = record_clip(LISTEN_SECONDS, device=self.device)
        results = analyze_chord(samples, sample_rate, self.expected_freqs)
        self.done.emit(results)


class ChordPracticeScreen(QWidget):
    def __init__(self, get_device: callable):
        super().__init__()
        self.get_device = get_device  # lets this tab reuse whatever mic the Tuner tab has selected
        self.worker = None

        self.chord_box = QComboBox()
        self.chord_box.addItems(CHORD_SHAPES.keys())
        self.chord_box.currentTextChanged.connect(self._on_chord_changed)

        self.diagram = ChordDiagramWidget()

        self.listen_button = QPushButton("Akkord testen (1,5s zuhören)")
        self.listen_button.clicked.connect(self._start_listening)

        self.status_label = QLabel("Wähle einen Akkord und drück auf testen.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)

        self.string_labels = []
        strings_row = QHBoxLayout()
        for name in STRING_NAMES:
            label = QLabel(name)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 6px;")
            strings_row.addWidget(label)
            self.string_labels.append(label)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Akkord:"))
        layout.addWidget(self.chord_box)
        layout.addWidget(self.diagram)
        layout.addWidget(self.listen_button)
        layout.addLayout(strings_row)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self._on_chord_changed(self.chord_box.currentText())

    def _on_chord_changed(self, name):
        self.diagram.set_chord(CHORD_SHAPES[name])
        for label in self.string_labels:
            label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 6px;")

    def _start_listening(self):
        self.listen_button.setEnabled(False)
        self.status_label.setText("Höre zu... jetzt den Akkord anschlagen.")
        expected = expected_frequencies(self.chord_box.currentText())
        self.worker = _ListenWorker(expected, self.get_device())
        self.worker.done.connect(self._on_result)
        self.worker.start()

    def _on_result(self, results):
        self.listen_button.setEnabled(True)
        for label, result in zip(self.string_labels, results):
            if result is None:
                style = "padding: 6px;"  # muted string, not checked
            elif result:
                style = "padding: 6px; background-color: #2f855a; color: white; border-radius: 4px;"
            else:
                style = "padding: 6px; background-color: #c53030; color: white; border-radius: 4px;"
            label.setStyleSheet(f"font-size: 16px; font-weight: bold; {style}")

        matched, total = chord_match_score(results)
        if matched == total:
            self.status_label.setText(f"Passt! Alle {total} Saiten erkannt.")
        else:
            self.status_label.setText(f"{matched} von {total} Saiten erkannt - rot markierte nochmal prüfen.")
