import os
import time
import sounddevice as sd
from scipy.io.wavfile import write
from google.cloud import speech
import firebase_admin
from firebase_admin import db
import RPi.GPIO as GPIO

# Button and audio config
BUTTON_PIN = 26
DURATION = 5
SAMPLE_RATE = 44100
CHANNELS = 1
AUDIO_PATH = "/home/pi/Desktop/code/recorded.wav"

# Set credentials for Google STT
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/Desktop/code/elaborate-leaf-461704-v6-183749559b24.json"

def stt_button_listener():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("STT listener running. Waiting for button press...")

    prev_state = GPIO.input(BUTTON_PIN)

    try:
        while True:
            current_state = GPIO.input(BUTTON_PIN)

            # Detect HIGH -> LOW (button press)
            if prev_state == GPIO.HIGH and current_state == GPIO.LOW:
                print("Button pressed.")
                record_audio(AUDIO_PATH)
                transcribe_audio(AUDIO_PATH)
                time.sleep(0.5)  # debounce

            prev_state = current_state
            time.sleep(0.05)  # polling interval
    except KeyboardInterrupt:
        print("STT listener terminated.")
    finally:
        GPIO.cleanup()

def record_audio(filename):
    print("Recording...")
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
    sd.wait()
    write(filename, SAMPLE_RATE, recording)
    print(f"Recording saved: {filename}")

def transcribe_audio(filename):
    client = speech.SpeechClient()
    with open(filename, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code="ko-KR"
    )
    response = client.recognize(config=config, audio=audio)
    if not response.results:
        print("No speech recognized.")
        return
    transcript = response.results[0].alternatives[0].transcript.replace(" ", "")
    print("Transcript:", transcript)
    db.reference('text').set(transcript)
    if any(word in transcript for word in ["살려주세요", "도와주세요"]):
        print("Emergency detected!")
        db.reference('emergency').set(True)
    else:
        print("No emergency detected.")
        db.reference('emergency').set(False)
