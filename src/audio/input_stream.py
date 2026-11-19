"""Microphone capture that reports the detected note via a callback."""
import sounddevice as sd
import numpy as np

from .pitch_detection import detect_pitch, freq_to_note_name

SAMPLE_RATE = 44100
BLOCK_SIZE = 2048


def list_input_devices() -> list[tuple[int, str]]:
    """Return (device_index, name) for every device with at least one input channel."""
    return [
        (i, d["name"])
        for i, d in enumerate(sd.query_devices())
        if d["max_input_channels"] > 0
    ]


def default_input_device() -> int:
    return sd.default.device[0]


class MicPitchListener:
    def __init__(self, on_note: callable, device: int | None = None):
        self.on_note = on_note
        self._stream = sd.InputStream(
            device=device,
            channels=1,
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            callback=self._callback,
        )

    def _callback(self, indata, frames, time_info, status):
        samples = indata[:, 0]
        freq = detect_pitch(samples, SAMPLE_RATE)
        note = freq_to_note_name(freq) if freq else None
        self.on_note(freq, note)

    def start(self):
        self._stream.start()

    def stop(self):
        self._stream.stop()
        self._stream.close()
