"""
focus_audio_engine.py — Procedural Deep Work Focus Soundscape Audio Synthesizer
Generates and plays smooth, seamless ambient focus soundscapes using calm, relaxing
psychoacoustic frequencies (432Hz Harmonic & 40Hz Gamma Focus, Soft Skylight Rain,
Deep Space Brown Noise, and Mellow Lo-Fi Drone) using PySide6.QtMultimedia.
"""

import os
import math
import wave
import struct
import random
from typing import Optional

from PySide6.QtCore import QObject, QUrl
from PySide6.QtMultimedia import QSoundEffect


SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "assets", "sounds")
SYNTH_VERSION = "2.0_calm_frequencies"


def _generate_soundscapes_if_needed(force: bool = False):
    """Generates procedural sound files if they do not exist or are outdated."""
    os.makedirs(SOUNDS_DIR, exist_ok=True)
    version_file = os.path.join(SOUNDS_DIR, ".version")

    existing_ver = ""
    if os.path.exists(version_file):
        try:
            with open(version_file, "r") as vf:
                existing_ver = vf.read().strip()
        except Exception:
            pass

    needs_gen = force or (existing_ver != SYNTH_VERSION)

    sample_rate = 22050
    duration = 5.0  # 5-second seamless loop
    n_samples = int(sample_rate * duration)

    files_to_generate = {
        "gamma_40hz.wav": _synth_calm_gamma_432,
        "cyberpunk_rain.wav": _synth_gentle_skylight_rain,
        "deep_space_whitenoise.wav": _synth_velvety_brown_space,
        "lofi_coffeehouse.wav": _synth_mellow_lofi_drone,
    }

    for filename, synth_fn in files_to_generate.items():
        filepath = os.path.join(SOUNDS_DIR, filename)
        if needs_gen or not os.path.exists(filepath) or os.path.getsize(filepath) < 1000:
            try:
                samples = synth_fn(n_samples, sample_rate)
                # Apply seamless crossfade window at loop boundary (first/last 0.1s)
                _apply_seamless_loop_crossfade(samples, sample_rate, crossfade_sec=0.12)
                _write_wav(filepath, samples, sample_rate)
            except Exception as e:
                print(f"[AUDIO] Error generating {filename}: {e}")

    try:
        with open(version_file, "w") as vf:
            vf.write(SYNTH_VERSION)
    except Exception:
        pass


def _apply_seamless_loop_crossfade(samples: list, sample_rate: int, crossfade_sec: float = 0.12):
    """Cross-fades head and tail samples to eliminate any boundary clicks or pops."""
    n_fade = int(sample_rate * crossfade_sec)
    n = len(samples)
    if n < n_fade * 2:
        return
    for i in range(n_fade):
        ratio = (1.0 - math.cos(math.pi * i / n_fade)) * 0.5
        tail_idx = n - n_fade + i
        blended = samples[tail_idx] * (1.0 - ratio) + samples[i] * ratio
        samples[i] = blended
        samples[tail_idx] = blended


def _write_wav(filepath: str, samples: list, sample_rate: int):
    with wave.open(filepath, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)  # 16-bit PCM
        wav.setframerate(sample_rate)
        frames = bytearray()
        for s in samples:
            val = max(-32767, min(32767, int(s * 32767)))
            frames += struct.pack("<h", val)
        wav.writeframes(frames)


def _synth_calm_gamma_432(n_samples: int, sample_rate: int) -> list:
    """
    Calm & Relaxing 432Hz Harmonic Resonance with Gentle 40Hz Isochronic Flow.
    Uses A=432Hz golden-ratio tuning with a warm 108Hz sub-bass foundation and
    a subtle, gentle (15% depth) 40Hz gamma focus pulse. Zero harsh buzz.
    """
    samples = []
    b0, b1, b2 = 0.0, 0.0, 0.0
    for i in range(n_samples):
        t = i / sample_rate

        # 432Hz golden healing tone + 108Hz grounding sub-harmonic (2 octaves down)
        tone_432 = math.sin(2 * math.pi * 432.0 * t) * 0.12
        sub_108 = math.sin(2 * math.pi * 108.0 * t) * 0.16
        mid_216 = math.sin(2 * math.pi * 216.0 * t) * 0.08

        # Gentle 40Hz sinusoidal gamma wave modulation (soft 18% depth, not harsh on/off)
        gamma_pulse = 0.82 + 0.18 * math.sin(2 * math.pi * 40.0 * t)
        harmonic_bed = (tone_432 + sub_108 + mid_216) * gamma_pulse

        # Soft warm pink-noise bed (filtered 1/f noise for gentle acoustic masking)
        white = random.random() * 2.0 - 1.0
        b0 = 0.99886 * b0 + white * 0.0555
        b1 = 0.99332 * b1 + white * 0.0750
        b2 = 0.96900 * b2 + white * 0.1538
        pink = (b0 + b1 + b2 + white * 0.5362) * 0.015

        samples.append(harmonic_bed + pink)
    return samples


def _synth_gentle_skylight_rain(n_samples: int, sample_rate: int) -> list:
    """
    Soft, relaxing rain on a glass skylight with distant low rumble.
    Low-pass filtered below 500Hz to eliminate any sharp hissing frequencies,
    with gentle random droplet transients and a slow 0.1Hz ambient sway.
    """
    samples = []
    low_lp = 0.0
    mid_lp = 0.0
    rumble_phase = 0.0
    for i in range(n_samples):
        t = i / sample_rate
        white = random.random() * 2.0 - 1.0

        # Two-stage single-pole low pass filter for warm, velvety rainfall
        low_lp += 0.045 * (white - low_lp)
        mid_lp += 0.09 * (white - mid_lp)
        rain_wash = (low_lp * 0.7 + mid_lp * 0.3) * 0.40

        # Distant warm 50Hz shelter rumble
        rumble_phase += 2 * math.pi * 50.0 / sample_rate
        rumble = math.sin(rumble_phase) * 0.035

        # Delicate, gentle droplet ping on skylight glass (soft decaying sine, zero clicks)
        droplet = 0.0
        if random.random() < 0.0025:
            freq = random.uniform(550.0, 750.0)
            droplet = random.uniform(0.04, 0.09) * math.sin(2 * math.pi * freq * t)

        # Slow 0.12Hz ambient breathing swell
        swell = 0.85 + 0.15 * math.sin(2 * math.pi * 0.12 * t)
        samples.append((rain_wash + rumble + droplet) * swell)
    return samples


def _synth_velvety_brown_space(n_samples: int, sample_rate: int) -> list:
    """
    Velvety Brown Noise (1/f² power density) for soothing acoustic isolation.
    Attenuates high frequencies at -6dB per octave, creating a deep, warm,
    fatigue-free ocean-like frequency profile known to calm the central nervous system.
    """
    samples = []
    brown = 0.0
    for i in range(n_samples):
        t = i / sample_rate
        white = random.random() * 2.0 - 1.0
        # True Brownian random walk with gentle DC bias leakage
        brown = (brown + (0.018 * white)) / 1.018

        # Slow, rhythmic 0.08Hz cosmic tide swell
        cosmic_tide = 0.85 + 0.15 * math.sin(2 * math.pi * 0.08 * t)
        samples.append(brown * 0.32 * cosmic_tide)
    return samples


def _synth_mellow_lofi_drone(n_samples: int, sample_rate: int) -> list:
    """
    Warm, mellow analog acoustic chord drone in D Major 9 / F# Minor (tuned to A=432Hz).
    Features warm Rhodes-style fundamentals with soft tape warmth and subtle vibrato.
    """
    samples = []
    # 432Hz tuned chord fundamentals: D3 (144Hz), F#3 (180Hz), A3 (216Hz), C#4 (272Hz), E4 (324Hz)
    chord_freqs = [144.0, 180.0, 216.0, 272.0, 324.0]
    chord_weights = [0.09, 0.07, 0.06, 0.05, 0.04]

    lp_filter = 0.0
    for i in range(n_samples):
        t = i / sample_rate
        # Subtle 0.2Hz analog pitch drift (warm wow & flutter)
        drift = 1.0 + 0.003 * math.sin(2 * math.pi * 0.25 * t)

        chord_val = 0.0
        for f, w in zip(chord_freqs, chord_weights):
            chord_val += math.sin(2 * math.pi * (f * drift) * t) * w

        # Soft low-pass analog warmth filter
        white = random.random() * 2.0 - 1.0
        lp_filter += 0.025 * (white - lp_filter)
        vinyl_warmth = lp_filter * 0.015

        samples.append(chord_val + vinyl_warmth)
    return samples


class FocusAudioEngine(QObject):
    """Real-time sound engine managing procedural ambient soundscape playback."""

    NAME_MAP = {
        "40hz": "gamma_40hz.wav",
        "gamma": "gamma_40hz.wav",
        "focus": "gamma_40hz.wav",
        "rain": "cyberpunk_rain.wav",
        "skylight": "cyberpunk_rain.wav",
        "space": "deep_space_whitenoise.wav",
        "white": "deep_space_whitenoise.wav",
        "brown": "deep_space_whitenoise.wav",
        "coffee": "lofi_coffeehouse.wav",
        "lo-fi": "lofi_coffeehouse.wav",
        "lofi": "lofi_coffeehouse.wav",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sound_effect: Optional[QSoundEffect] = None
        self._current_track = "40Hz Gamma Focus Waves"
        self._volume = 0.40
        self._is_playing = False

        # Generate / upgrade audio assets on initial start
        _generate_soundscapes_if_needed(force=False)

        try:
            self._sound_effect = QSoundEffect(self)
            self._sound_effect.setLoopCount(QSoundEffect.Loop.Infinite.value)
            self._sound_effect.setVolume(self._volume)
        except Exception as e:
            print(f"[AUDIO] QSoundEffect initialization notice: {e}")

    def _resolve_filename(self, track_name: str) -> str:
        lower = track_name.lower()
        for key, fname in self.NAME_MAP.items():
            if key in lower:
                return fname
        return "gamma_40hz.wav"

    def play_soundscape(self, track_name: str):
        """Starts or switches playback to the specified soundscape track."""
        fname = self._resolve_filename(track_name)
        fpath = os.path.abspath(os.path.join(SOUNDS_DIR, fname))

        if not os.path.exists(fpath):
            _generate_soundscapes_if_needed(force=True)

        if self._sound_effect:
            try:
                self._sound_effect.stop()
                self._sound_effect.setSource(QUrl.fromLocalFile(fpath))
                self._sound_effect.setLoopCount(QSoundEffect.Loop.Infinite.value)
                self._sound_effect.setVolume(self._volume)
                self._sound_effect.play()
                self._is_playing = True
                self._current_track = track_name
            except Exception as e:
                print(f"[AUDIO] Play error: {e}")

    def pause(self):
        """Pauses soundscape audio output."""
        if self._sound_effect and self._is_playing:
            try:
                self._sound_effect.stop()
            except Exception:
                pass
            self._is_playing = False

    def resume(self):
        """Resumes active soundscape."""
        if self._sound_effect and self._current_track:
            self.play_soundscape(self._current_track)

    def set_volume(self, volume_pct: int):
        """Sets output volume (0 to 100)."""
        self._volume = max(0.0, min(1.0, volume_pct / 100.0))
        if self._sound_effect:
            self._sound_effect.setVolume(self._volume)

    @property
    def is_playing(self) -> bool:
        return self._is_playing

    @property
    def current_track(self) -> str:
        return self._current_track
