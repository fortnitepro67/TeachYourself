"""Standard guitar tuning reference."""

STANDARD_TUNING = {
    6: "E2",
    5: "A2",
    4: "D3",
    3: "G3",
    2: "B3",
    1: "E4",
}

# Exact target frequencies for the 6 open strings, keyed by note name.
# Used to match a detected pitch against the correct string+octave instead
# of just the nearest chromatic note (which can pick the wrong octave when
# a string is badly out of tune).
STANDARD_TUNING_FREQS = {
    "E2": 82.41,
    "A2": 110.00,
    "D3": 146.83,
    "G3": 196.00,
    "B3": 246.94,
    "E4": 329.63,
}

# Same 6 open-string frequencies, but as a plain list ordered low E to high
# e - matches the string order used by CHORD_SHAPES / STRING_NAMES.
OPEN_STRING_FREQS = [82.41, 110.00, 146.83, 196.00, 246.94, 329.63]
