import sys
sys.path.append(".")

from src.content.chords import CHORD_SHAPES


def test_every_chord_has_six_strings_with_valid_frets():
    for name, shape in CHORD_SHAPES.items():
        assert len(shape) == 6, f"{name} must have 6 entries"
        for fret in shape:
            assert fret is None or (isinstance(fret, int) and fret >= 0), f"{name} has invalid fret {fret}"


if __name__ == "__main__":
    test_every_chord_has_six_strings_with_valid_frets()
    print("ok")
