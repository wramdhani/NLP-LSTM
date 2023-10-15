from flask import render_template, Flask, request
from process import model, generate_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('website/index.html')

@app.route('/get')
def get_response():
    user_input = str(request.args.get('msg'))
    result = generate_response(user_input)
    return result

if __name__ == '__main__':
    app.run(
        host="localhost",
        port=8080,
        debug=True
    )
    