from flask import Blueprint, render_template, session, request
from process import generate_response

views = Blueprint(
    'views', __name__,
    template_folder="../templates",
    static_folder="../static")

@views.route('/')
def home():
  return render_template("index.html")

@views.route('/chat', methods=['POST', 'GET'])
def chat():
    if 'messages' not in session:
        session['messages'] = []
    if request.method == 'POST':
        user_input = request.form['msg']
        session['messages'].append({'class': 'user-message', 'text': user_input})
        session['messages'].append({'class': 'bot-message', 'text': generate_response(user_input)})
    return render_template("chatInterface.html", messages=session['messages'])