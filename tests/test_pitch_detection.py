import numpy as np
import sys
sys.path.append(".")

from src.audio.pitch_detection import detect_pitch, freq_to_note_name


def _sine(freq, sample_rate=44100, duration=0.1):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return np.sin(2 * np.pi * freq * t)


def test_detects_low_e_string():
    samples = _sine(82.41)  # E2, guitar's lowest open string
    freq = detect_pitch(samples, 44100)
    assert freq is not None
    assert abs(freq - 82.41) < 1.0
    assert freq_to_note_name(freq) == "E2"


def test_detects_high_e_string():
    samples = _sine(329.63)  # E4, guitar's highest open string
    freq = detect_pitch(samples, 44100)
    assert freq is not None
    assert freq_to_note_name(freq) == "E4"


def test_silence_returns_none():
    samples = np.zeros(4096)
    assert detect_pitch(samples, 44100) is None


if __name__ == "__main__":
    test_detects_low_e_string()
    test_detects_high_e_string()
    test_silence_returns_none()
    print("all tests passed")
