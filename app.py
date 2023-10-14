from flask import render_template, Flask
from process import model

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('website/index.html')

if __name__ == '__main__':
    app.run(host="localhost", port=8080)