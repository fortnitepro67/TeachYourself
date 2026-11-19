"""Autocorrelation-based pitch detection (no C-extension deps)."""
import numpy as np

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def detect_pitch(samples: np.ndarray, sample_rate: int, min_hz: float = 70.0, max_hz: float = 1200.0) -> float | None:
    """Return the fundamental frequency in Hz, or None if no clear pitch is found."""
    samples = samples.astype(np.float64)
    samples -= samples.mean()
    if np.max(np.abs(samples)) < 1e-4:
        return None  # silence

    min_lag = int(sample_rate / max_hz)
    max_lag = int(sample_rate / min_hz)
    if max_lag >= len(samples):
        return None

    corr = np.correlate(samples, samples, mode="full")
    corr = corr[len(corr) // 2:]
    # Raw autocorrelation is biased toward small lags because fewer samples
    # overlap at larger lags. Normalize by the overlap count so periodicity
    # at low frequencies isn't swamped by that near-zero-lag bias.
    overlap_counts = len(samples) - np.arange(len(corr))
    corr = corr / overlap_counts

    search = corr[min_lag:max_lag]
    if search.size == 0 or corr[0] <= 0:
        return None

    # Take the FIRST local peak above the confidence threshold, not the
    # global max: for a clean tone, every multiple of the true period
    # correlates equally well, so the global max can land on an overtone
    # (octave error) instead of the fundamental.
    threshold = 0.3
    peak_idx = None
    for i in range(1, len(search) - 1):
        if search[i] >= search[i - 1] and search[i] > search[i + 1] and search[i] / corr[0] > threshold:
            peak_idx = i
            break
    if peak_idx is None:
        return None

    peak_lag = min_lag + peak_idx
    return sample_rate / peak_lag


def freq_to_note_name(freq: float) -> str:
    """Convert a frequency to the nearest note name + octave, e.g. 'E2'."""
    a4 = 440.0
    semitones_from_a4 = round(12 * np.log2(freq / a4))
    midi = 69 + semitones_from_a4
    octave = midi // 12 - 1
    name = NOTE_NAMES[midi % 12]
    return f"{name}{octave}"
