import numpy as np
import sys
sys.path.append(".")

from src.audio.chord_detection import analyze_chord, chord_match_score
from src.content.chords import expected_frequencies


def _mix(freqs, sample_rate=44100, duration=1.0):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.zeros_like(t)
    for f in freqs:
        signal += np.sin(2 * np.pi * f * t)
    return signal


def test_correct_em_chord_matches_all_strings():
    expected = expected_frequencies("Em")  # [82.41, 2 semitones up A, 2 semitones up D, 196.0, 246.94, 329.63]
    played_freqs = [f for f in expected if f is not None]
    samples = _mix(played_freqs)

    results = analyze_chord(samples, 44100, expected)
    matched, total = chord_match_score(results)
    assert matched == total
    assert total == 6  # Em has no muted strings


def test_missing_string_is_detected():
    expected = expected_frequencies("Em")
    played_freqs = [f for f in expected if f is not None][1:]  # skip the low E string
    samples = _mix(played_freqs)

    results = analyze_chord(samples, 44100, expected)
    matched, total = chord_match_score(results)
    assert matched == total - 1
    assert results[0] == False  # low E string missing


def test_muted_strings_are_not_checked():
    expected = expected_frequencies("A")  # low E string is muted in open A
    assert expected[0] is None
    played_freqs = [f for f in expected if f is not None]
    samples = _mix(played_freqs)

    results = analyze_chord(samples, 44100, expected)
    assert results[0] is None


def _pluck(freq, sample_rate=44100, duration=1.0, n_harmonics=6, amp=1.0):
    """A string pluck has a fundamental plus decaying harmonics, unlike a pure sine."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sig = np.zeros_like(t)
    for n in range(1, n_harmonics + 1):
        sig += amp * (1 / n) * np.sin(2 * np.pi * freq * n * t + 0.3 * n)
    return sig


def test_misfretted_string_not_falsely_matched_via_other_strings_harmonic():
    # Fretting the D string at fret 2 (E3, 164.81Hz) lands almost exactly on
    # the open low E string's 2nd harmonic (2*82.41=164.82Hz). Leaving the D
    # string unfretted (open, 146.83Hz instead) must not still read as a
    # match just because the low E string's harmonic rings at the same spot.
    expected = expected_frequencies("Em")
    open_d = 146.83
    played = [expected[0], expected[1], open_d, expected[3], expected[4], expected[5]]
    samples = sum(_pluck(f) for f in played)

    results = analyze_chord(samples, 44100, expected)
    assert results[2] == False


def test_quietest_real_string_in_a_mix_is_still_matched():
    expected = expected_frequencies("Em")
    played = [f for f in expected if f is not None]
    amps = [1.0, 0.6, 0.5, 0.8, 0.4, 0.9]  # uneven pluck strength, as on a real guitar
    samples = sum(_pluck(f, amp=a) for f, a in zip(played, amps))

    results = analyze_chord(samples, 44100, expected)
    matched, total = chord_match_score(results)
    assert matched == total


def test_silence_matches_nothing():
    expected = expected_frequencies("Em")
    samples = np.zeros(44100)
    results = analyze_chord(samples, 44100, expected)
    matched, total = chord_match_score(results)
    assert matched == 0


if __name__ == "__main__":
    test_correct_em_chord_matches_all_strings()
    test_missing_string_is_detected()
    test_muted_strings_are_not_checked()
    test_silence_matches_nothing()
    print("ok")
