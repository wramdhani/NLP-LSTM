from process import preparation
from website import create_app

app = create_app()

#download nltk
preparation()

if __name__ == "__main__":
    app.run(
        host="localhost",
        port=8080,
        debug=True
    )
