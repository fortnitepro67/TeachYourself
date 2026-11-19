"""Open chord shapes for guitar: fret per string, ordered low E (string 6) to high E (string 1).
None = muted string, 0 = open string, N = fret N.
"""

CHORD_SHAPES = {
    "E":  [0, 2, 2, 1, 0, 0],
    "Em": [0, 2, 2, 0, 0, 0],
    "A":  [None, 0, 2, 2, 2, 0],
    "Am": [None, 0, 2, 2, 1, 0],
    "D":  [None, None, 0, 2, 3, 2],
    "Dm": [None, None, 0, 2, 3, 1],
    "C":  [None, 3, 2, 0, 1, 0],
    "G":  [3, 2, 0, 0, 0, 3],
}
