"""Theory tab: browse open chord diagrams."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QCheckBox
from PySide6.QtCore import Qt

from src.content.chords import CHORD_SHAPES
from src.ui.chord_diagram import ChordDiagramWidget


class TheoryScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.chord_box = QComboBox()
        self.chord_box.addItems(CHORD_SHAPES.keys())
        self.chord_box.currentTextChanged.connect(self._on_chord_changed)

        self.finger_checkbox = QCheckBox("Fingernummern anzeigen")
        self.finger_checkbox.toggled.connect(self._on_fingers_toggled)

        self.diagram = ChordDiagramWidget()

        hint = QLabel(
            "Die Buchstaben oben sind die Saiten (von links = tiefste Saite bis "
            "rechts = höchste Saite). x = Saite nicht anschlagen. o = Saite "
            "leer (ohne Finger) spielen. Ein Punkt bedeutet: in diesem Bund mit "
            "einem Finger herunterdrücken, genau auf dieser Saite. Mit der "
            "Checkbox siehst du, welcher Finger empfohlen wird "
            "(1 = Zeigefinger, 2 = Mittelfinger, 3 = Ringfinger, 4 = kleiner Finger)."
        )
        hint.setAlignment(Qt.AlignCenter)
        hint.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Akkord:"))
        layout.addWidget(self.chord_box)
        layout.addWidget(self.finger_checkbox)
        layout.addWidget(self.diagram)
        layout.addWidget(hint)
        self.setLayout(layout)

        self._on_chord_changed(self.chord_box.currentText())

    def _on_chord_changed(self, name):
        self.diagram.set_chord(CHORD_SHAPES[name])

    def _on_fingers_toggled(self, checked):
        self.diagram.set_show_fingers(checked)
