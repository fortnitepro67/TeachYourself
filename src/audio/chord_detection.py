"""Checks whether a recorded clip contains the frequencies of a target chord.

Unlike the tuner (one pitch at a time via YIN), a strummed chord has several
strings ringing together, so instead of trying to fully separate every note
we just check whether there is a spectral peak near each string's expected
frequency - simpler and robust as long as we know what chord is being tested.
"""
import numpy as np


def analyze_chord(samples: np.ndarray, sample_rate: int, expected_freqs: list[float | None], tolerance_cents: float = 35.0, presence_fraction: float = 0.35) -> list[bool | None]:
    """Return, per string, True/False whether that string's expected pitch
    seems present, or None for a muted string (not checked).

    "Present" means the spectral peak near that frequency reaches at least
    `presence_fraction` of the overall spectrum's peak. A fixed noise floor
    (e.g. the spectrum's median) doesn't work: on a near-silent background a
    real string's energy is still a million times the median, but so is mere
    windowing leakage from the OTHER strings into an unplayed string's bin -
    comparing against the loudest string actually playing separates the two.

    shortcut: a fretted note that happens to sit near-exactly on another
    playing string's harmonic (e.g. fretting the D string at the 2nd fret
    gives E3, almost exactly the open low E string's 2nd harmonic) can still
    read as present even when misfretted/not played - real harmonic energy
    from the other string lands right on the target bin. presence_fraction
    0.35 rejects most incidental harmonic bleed while still accepting quieter
    real strings, but doesn't fully solve it; a real fix needs per-string
    harmonic-series/inharmonicity analysis, not just single-bin energy.
    """
    samples = samples.astype(np.float64)
    samples = samples - samples.mean()

    window = np.hanning(len(samples))
    spectrum = np.abs(np.fft.rfft(samples * window))
    freq_axis = np.fft.rfftfreq(len(samples), 1 / sample_rate)
    global_peak = spectrum.max()
    if global_peak <= 0:
        return [None if f is None else False for f in expected_freqs]

    tol_ratio = 2 ** (tolerance_cents / 1200)
    results: list[bool | None] = []
    for target in expected_freqs:
        if target is None:
            results.append(None)
            continue
        mask = (freq_axis >= target / tol_ratio) & (freq_axis <= target * tol_ratio)
        peak = spectrum[mask].max() if mask.any() else 0.0
        results.append(peak > global_peak * presence_fraction)
    return results


def chord_match_score(results: list[bool | None]) -> tuple[int, int]:
    """(matched, total) over the non-muted strings."""
    checked = [r for r in results if r is not None]
    return sum(checked), len(checked)
