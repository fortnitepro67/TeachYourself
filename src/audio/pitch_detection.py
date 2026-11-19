"""YIN-based pitch detection (pure numpy, no C-extension deps).

Plain autocorrelation picks whichever period correlates strongest, and for
real instrument tones (rich in harmonics) that is often an overtone's period
rather than the true fundamental, causing octave errors. YIN's cumulative
mean normalized difference function specifically suppresses those overtone
matches, so it tracks the true fundamental of real (not just pure-sine) tones.
"""
import numpy as np

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def detect_pitch(samples: np.ndarray, sample_rate: int, min_hz: float = 70.0, max_hz: float = 1200.0, threshold: float = 0.15) -> float | None:
    """Return the fundamental frequency in Hz, or None if no clear pitch is found."""
    samples = samples.astype(np.float64)
    samples -= samples.mean()
    if np.max(np.abs(samples)) < 1e-4:
        return None  # silence

    min_lag = max(int(sample_rate / max_hz), 1)
    max_lag = int(sample_rate / min_hz)
    n = len(samples)
    if max_lag >= n:
        return None

    diff = np.zeros(max_lag + 1)
    for tau in range(1, max_lag + 1):
        delta = samples[: n - tau] - samples[tau:]
        diff[tau] = np.dot(delta, delta)

    cmnd = np.ones(max_lag + 1)
    running_sum = 0.0
    for tau in range(1, max_lag + 1):
        running_sum += diff[tau]
        cmnd[tau] = diff[tau] * tau / running_sum if running_sum > 0 else 1.0

    tau = None
    for t in range(min_lag, max_lag + 1):
        if cmnd[t] < threshold:
            while t + 1 <= max_lag and cmnd[t + 1] < cmnd[t]:
                t += 1
            tau = t
            break
    if tau is None:
        return None

    return sample_rate / tau


def freq_to_note_name(freq: float) -> str:
    """Convert a frequency to the nearest note name + octave, e.g. 'E2'."""
    a4 = 440.0
    semitones_from_a4 = round(12 * np.log2(freq / a4))
    midi = 69 + semitones_from_a4
    octave = midi // 12 - 1
    name = NOTE_NAMES[midi % 12]
    return f"{name}{octave}"


def cents_off(freq: float, target_freq: float) -> float:
    """How many cents freq is above (+) or below (-) target_freq."""
    return 1200 * np.log2(freq / target_freq)


def nearest_note(freq: float) -> tuple[str, float, float]:
    """Nearest named note for freq: (name, that note's exact frequency, cents off)."""
    a4 = 440.0
    semitones_from_a4 = round(12 * np.log2(freq / a4))
    target_freq = a4 * 2 ** (semitones_from_a4 / 12)
    return freq_to_note_name(freq), target_freq, cents_off(freq, target_freq)
