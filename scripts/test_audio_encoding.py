# %%
from io import BytesIO

import pyaudio
import wave
import numpy as np

# %%
# AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 1
BURN_IN = 3
WAVE_OUTPUT_FILENAME = "output.wav"

def load_stream(data):
    with BytesIO() as DATA_BYTES:
        with wave.open(DATA_BYTES, "wb") as waveFile:
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(data)
        DATA_BYTES.seek(0)
        with wave.open(DATA_BYTES, "r") as spf:
            signal = spf.readframes(-1)
            signal = np.frombuffer(signal, np.int16)
    return signal

# %%
audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

frames = []
chunki = 0
started = False
while True:
    chunk_data = []
    CHUNK_BYTES = BytesIO()
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        chunk_data.append(data)
    datastream = load_stream(b"".join(chunk_data))
    gotaudio = np.mean(np.abs(datastream).astype(float)) >= 500
    print(gotaudio)
    if gotaudio:
        chunki = 0
        if not started:
            started = True
    else:
        if started:
            chunki += 1
        if chunki > BURN_IN:
            break
    if started:
        frames.extend(chunk_data)
    print(len(chunk_data))    
    print(len(frames))
    print(chunki)

with wave.open(WAVE_OUTPUT_FILENAME, "wb") as waveFile:
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b"".join(frames))

stream.stop_stream()
stream.close()
audio.terminate()
