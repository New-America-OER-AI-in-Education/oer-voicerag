from io import BytesIO

from openai import OpenAI
import pyaudio
import wave
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

# AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 0.2
WAIT_CHUNKS = 10
WAVE_OUTPUT_FILENAME = "output.wav"


def load_stream(data, sample_size):
    with BytesIO() as DATA_BYTES:
        with wave.open(DATA_BYTES, "wb") as waveFile:
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(sample_size)
            waveFile.setframerate(RATE)
            waveFile.writeframes(data)
        DATA_BYTES.seek(0)
        with wave.open(DATA_BYTES, "r") as spf:
            signal = spf.readframes(-1)
            signal = np.frombuffer(signal, np.int16)
    return signal


def listen_for_input(verbose=0):
    audio = pyaudio.PyAudio()
    sample_size = audio.get_sample_size(FORMAT)

    # start Recording
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    frames = []
    chunki = 0
    started = False
    while True:
        chunk_data = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            chunk_data.append(data)
        datastream = load_stream(b"".join(chunk_data), sample_size)
        gotaudio = np.mean(np.abs(datastream).astype(float)) >= 500
        if verbose > 0:
            print(gotaudio)
        if gotaudio:
            chunki = 0
            if not started:
                started = True
        else:
            if started:
                chunki += 1
            if chunki > WAIT_CHUNKS:
                break
        if started:
            frames.extend(chunk_data)
        if verbose > 0:
            print(len(chunk_data))
            print(len(frames))
            print(chunki)

    with wave.open(WAVE_OUTPUT_FILENAME, "wb") as waveFile:
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(sample_size)
        waveFile.setframerate(RATE)
        waveFile.writeframes(b"".join(frames))

    stream.stop_stream()
    stream.close()
    audio.terminate()


def play_text(text, model="tts-1", voice="alloy"):
    client = OpenAI()
    response = client.audio.speech.create(
        model=model, voice=voice, input=text, response_format="mp3"
    )
    response.write_to_file("speech.mp3")
    resp = AudioSegment.from_mp3("speech.mp3")
    play(resp)


def transcribe_input():
    listen_for_input()
    client = OpenAI()

    with open("output.wav", "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )
    return transcription
