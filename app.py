

from flask import Flask, render_template, Response
from PIL import Image
import io
import imageio

app = Flask(__name__)

def generate_frames():
    camera = imageio.get_reader("<video0>", format="ffmpeg")
    for frame in camera:
        # imageioのフレームをPillowのImageオブジェクトに変換
        image = Image.fromarray(frame)
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        frame = buffer.getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/viewer1')
def viewer1():
    return render_template('viewer1.html')

@app.route('/viewer2')
def viewer2():
    return render_template('viewer2.html')

if __name__ == '__main__':
    app.run(debug=True)