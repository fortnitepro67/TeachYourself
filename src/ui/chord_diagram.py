"""Draws a simple open-chord fretboard diagram (6 strings x 4 frets)."""
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt

from src.content.chords import STRING_NAMES

FRETS_SHOWN = 4
MARGIN_SIDE = 30
MARGIN_TOP = 55  # room for string names + open/muted markers above the nut
MARGIN_BOTTOM = 15


class ChordDiagramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.shape = None
        self.show_fingers = False
        self.setMinimumSize(220, 260)

    def set_chord(self, shape):
        self.shape = shape
        self.update()

    def set_show_fingers(self, show: bool):
        self.show_fingers = show
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        grid_w = w - 2 * MARGIN_SIDE
        grid_h = h - MARGIN_TOP - MARGIN_BOTTOM
        string_gap = grid_w / 5
        fret_gap = grid_h / FRETS_SHOWN

        font = QFont()
        font.setPointSize(11)
        painter.setFont(font)

        # String names above everything, so it's unambiguous which column is which string
        pen = QPen(QColor("#333333"))
        painter.setPen(pen)
        for s, label in enumerate(STRING_NAMES):
            x = MARGIN_SIDE + s * string_gap
            painter.drawText(int(x - 6), 18, label)

        # frets (thick line = nut, i.e. open end of the neck)
        for f in range(FRETS_SHOWN + 1):
            y = MARGIN_TOP + f * fret_gap
            pen.setWidth(5 if f == 0 else 1)
            painter.setPen(pen)
            painter.drawLine(int(MARGIN_SIDE), int(y), int(MARGIN_SIDE + grid_w), int(y))

        # strings (vertical)
        pen.setWidth(1)
        painter.setPen(pen)
        for s in range(6):
            x = MARGIN_SIDE + s * string_gap
            painter.drawLine(int(x), int(MARGIN_TOP), int(x), int(MARGIN_TOP + grid_h))

        if not self.shape:
            painter.end()
            return

        for s, (fret, finger) in enumerate(self.shape):
            x = MARGIN_SIDE + s * string_gap
            if fret is None:
                painter.drawText(int(x - 5), MARGIN_TOP - 10, "x")
            elif fret == 0:
                painter.drawText(int(x - 5), MARGIN_TOP - 10, "o")
            else:
                y = MARGIN_TOP + (fret - 0.5) * fret_gap
                painter.setBrush(QColor("#2b6cb0"))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(int(x - 9), int(y - 9), 18, 18)
                if self.show_fingers and finger is not None:
                    painter.setPen(QColor("white"))
                    painter.drawText(int(x - 4), int(y + 4), str(finger))
                painter.setPen(pen)

        painter.end()
