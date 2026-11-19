"""Open chord shapes for guitar, ordered low E (string 6) to high e (string 1).

Each string entry is (fret, finger):
- fret: None (muted), 0 (open), or the fret number to press.
- finger: which finger to use (1=index, 2=middle, 3=ring, 4=pinky), or None
  when the string is open/muted.
"""

STRING_NAMES = ["E", "A", "D", "G", "B", "e"]

CHORD_SHAPES = {
    "E":  [(0, None), (2, 2), (2, 3), (1, 1), (0, None), (0, None)],
    "Em": [(0, None), (2, 2), (2, 3), (0, None), (0, None), (0, None)],
    "A":  [(None, None), (0, None), (2, 1), (2, 2), (2, 3), (0, None)],
    "Am": [(None, None), (0, None), (2, 2), (2, 3), (1, 1), (0, None)],
    "D":  [(None, None), (None, None), (0, None), (2, 1), (3, 3), (2, 2)],
    "Dm": [(None, None), (None, None), (0, None), (2, 2), (3, 3), (1, 1)],
    "C":  [(None, None), (3, 3), (2, 2), (0, None), (1, 1), (0, None)],
    "G":  [(3, 2), (2, 1), (0, None), (0, None), (0, None), (3, 3)],
}
