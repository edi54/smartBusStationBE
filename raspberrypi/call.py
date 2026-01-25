import socket
import threading
import pyaudio
import time
from firebase_admin import db

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
PORT = 50007
SERVER_IP = '192.168.137.1'

call_active = False
conn = None
p = None
input_stream = None
output_stream = None

def init_audio():
    global p, input_stream, output_stream
    p = pyaudio.PyAudio()
    input_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    output_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

def close_audio():
    global p, input_stream, output_stream
    if input_stream: input_stream.stop_stream(); input_stream.close()
    if output_stream: output_stream.stop_stream(); output_stream.close()
    if p: p.terminate()

def connect_to_server():
    global conn
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((SERVER_IP, PORT))
        return True
    except:
        return False

def close_connection():
    global conn
    if conn:
        try: conn.shutdown(socket.SHUT_RDWR)
        except: pass
        conn.close()
        conn = None

def send_audio():
    while call_active and conn:
        try:
            data = input_stream.read(CHUNK, exception_on_overflow=False)
            conn.sendall(data)
        except:
            break

def receive_audio():
    while call_active and conn:
        try:
            data = conn.recv(CHUNK)
            if not data:
                break
            output_stream.write(data)
        except:
            break

def start_voice_chat():
    global call_active
    if call_active:
        return
    if not connect_to_server():
        return
    init_audio()
    call_active = True
    threading.Thread(target=send_audio, daemon=True).start()
    threading.Thread(target=receive_audio, daemon=True).start()

def stop_voice_chat():
    global call_active
    if not call_active:
        return
    call_active = False
    time.sleep(0.5)
    close_audio()
    close_connection()

def start_call_monitor():
    call_ref = db.reference('call')

    def listener(event):
        value = call_ref.get()
        if value == 1:
            start_voice_chat()
        else:
            stop_voice_chat()

    call_ref.listen(listener)
