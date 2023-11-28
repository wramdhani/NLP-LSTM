from flask import Flask, render_template, request
from process import preparation, generate_response

app = Flask(
    __name__,
    template_folder="website/templates",
    static_folder="website/static"
)

#download nltk
preparation()

@app.route('/')
def home():
    return render_template("chatInterface.html")

@app.route('/get')
def get_bot_response():
    user_input = request.args.get('msg')
    return str(generate_response(user_input))

if __name__ == "__main__":
    app.run(
        host="localhost",
        port=8080,
        debug=True
    )