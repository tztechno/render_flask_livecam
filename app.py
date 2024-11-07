from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/viewer1')
def viewer1():
    return render_template('viewer1.html')

@app.route('/viewer2')
def viewer2():
    return render_template('viewer2.html')

if __name__ == '__main__':
    app.run(debug=True)
