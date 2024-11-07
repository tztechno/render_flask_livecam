from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# 接続中のクライアント管理
clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/viewer1')
def viewer1():
    return render_template('viewer1.html')

@app.route('/viewer2')
def viewer2():
    return render_template('viewer2.html')

@socketio.on('connect')
def handle_connect():
    clients[request.sid] = {'type': None}
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in clients:
        del clients[request.sid]
        print(f'Client disconnected: {request.sid}')

@socketio.on('register')
def handle_register(data):
    clients[request.sid]['type'] = data['type']
    print(f'Client {request.sid} registered as {data["type"]}')

@socketio.on('offer')
def handle_offer(data):
    emit('offer', data, broadcast=True, skip_sid=request.sid)
    print(f'Offer received and broadcasted from {request.sid}')

@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, broadcast=True, skip_sid=request.sid)
    print(f'Answer received and broadcasted from {request.sid}')

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    emit('ice_candidate', data, broadcast=True, skip_sid=request.sid)
    print(f'ICE candidate received and broadcasted from {request.sid}')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
