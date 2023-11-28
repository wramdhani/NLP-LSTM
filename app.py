import os
from flask import Flask, render_template, request, session
from flask_session import Session  # Import the Session object
from process import preparation, generate_response

app = Flask(
    __name__,
    template_folder="website/templates",
    static_folder="website/static"
)

# Set the secret key and configure the session to use filesystem storage
app.config['SECRET_KEY'] = os.urandom(16)
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)  # Initialize the session

#download nltk
preparation()

@app.route('/', methods=['POST', 'GET'])
def home():
    if 'messages' not in session:
        session['messages'] = []
    if request.method == 'POST':
        user_input = request.form['msg']
        session['messages'].append({'class': 'user-message', 'text': user_input})
        session['messages'].append({'class': 'bot-message', 'text': generate_response(user_input)})
    return render_template("chatInterface.html", messages=session['messages'])

if __name__ == "__main__":
    app.run(
        host="localhost",
        port=8080,
        debug=True
    )
