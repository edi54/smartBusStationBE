from flask import Flask, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

picam2 = Picamera2()


video_config = picam2.create_video_configuration(
    main={"size": (1920, 1080)}  
)
picam2.configure(video_config)

picam2.set_controls({
    "AwbMode": 0,
    "ColourGains": (2.2, 1.7)
})
picam2.start()

def generate_frames():
    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream')
def stream():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
    <h1>Camera Module 3 Stream</h1>
    <img src="/stream" style="max-width: 100%; height: auto;">
    '''

def create_app():
    return app
