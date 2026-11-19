import sys
sys.path.append(".")

from src.content.chords import CHORD_SHAPES, STRING_NAMES


def test_every_chord_has_six_strings_with_valid_entries():
    assert len(STRING_NAMES) == 6
    for name, shape in CHORD_SHAPES.items():
        assert len(shape) == 6, f"{name} must have 6 entries"
        for fret, finger in shape:
            assert fret is None or (isinstance(fret, int) and fret >= 0), f"{name} has invalid fret {fret}"
            assert finger is None or finger in (1, 2, 3, 4), f"{name} has invalid finger {finger}"
            if fret is None or fret == 0:
                assert finger is None, f"{name}: open/muted string can't have a finger"


if __name__ == "__main__":
    test_every_chord_has_six_strings_with_valid_entries()
    print("ok")
