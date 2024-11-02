from flask import Flask, render_template, Response
import imageio
from PIL import Image
import io

app = Flask(__name__)

def generate_frames():
    camera = imageio.get_reader('<video0>')  # デフォルトカメラを取得
    while True:
        frame = camera.get_next_data()  # フレームを取得
        # PILを使って画像を処理（必要に応じて）
        image = Image.fromarray(frame)  
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')  # JPEGフォーマットで保存
        frame = buffer.getvalue()  # バイナリデータを取得
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/viewer1')
def viewer1():
    return render_template('viewer1.html')

@app.route('/viewer2')
def viewer2():
    return render_template('viewer2.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)