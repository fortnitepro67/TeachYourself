"""Microphone capture that reports the detected note via a callback."""
import sounddevice as sd
import numpy as np

from .pitch_detection import detect_pitch, freq_to_note_name

BLOCK_DURATION = 2048 / 44100  # ~46ms: enough full periods to detect guitar's lowest open string


def _preferred_hostapi() -> int:
    """Windows reports the same physical device once per audio driver
    (MME, DirectSound, WASAPI, WDM-KS...), which duplicates every entry in
    the device list. Pick one driver - WASAPI if available - to show each
    device exactly once."""
    hostapis = sd.query_hostapis()
    for preferred in ("Windows WASAPI", "MME"):
        for i, api in enumerate(hostapis):
            if api["name"] == preferred:
                return i
    return 0


def list_input_devices() -> list[tuple[int, str]]:
    """Return (device_index, name) for every input device on the preferred driver."""
    hostapi = _preferred_hostapi()
    return [
        (i, d["name"])
        for i, d in enumerate(sd.query_devices())
        if d["max_input_channels"] > 0 and d["hostapi"] == hostapi
    ]


def default_input_device() -> int:
    hostapi = _preferred_hostapi()
    return sd.query_hostapis()[hostapi]["default_input_device"]


def record_clip(duration_seconds: float, device: int | None = None) -> tuple[np.ndarray, int]:
    """Blocking recording of a single mono clip. Call this off the UI thread
    (e.g. in a QThread) so it doesn't freeze the GUI for `duration_seconds`."""
    if device is None:
        device = default_input_device()
    sample_rate = int(sd.query_devices(device)["default_samplerate"])
    recording = sd.rec(int(duration_seconds * sample_rate), samplerate=sample_rate, channels=1, device=device)
    sd.wait()
    return recording[:, 0], sample_rate


class MicPitchListener:
    def __init__(self, on_note: callable, device: int | None = None):
        self.on_note = on_note
        if device is None:
            device = default_input_device()
        # Devices don't all support the same sample rate (e.g. some mics
        # only do 48000Hz, not the common 44100Hz), so use the device's own
        # native rate instead of a hardcoded one.
        self.sample_rate = int(sd.query_devices(device)["default_samplerate"])
        block_size = int(self.sample_rate * BLOCK_DURATION)
        self._stream = sd.InputStream(
            device=device,
            channels=1,
            samplerate=self.sample_rate,
            blocksize=block_size,
            callback=self._callback,
        )

    def _callback(self, indata, frames, time_info, status):
        samples = indata[:, 0]
        freq = detect_pitch(samples, self.sample_rate)
        note = freq_to_note_name(freq) if freq else None
        self.on_note(freq, note)

    def start(self):
        self._stream.start()

    def stop(self):
        self._stream.stop()
        self._stream.close()
