from flask import Flask

app = Flask(__name__)


@app.route("/create_session")
def create_session():
    return "Hello, World!"


@app.route("/get_response")
def get_response():
    return "Hello, World!"



if __name__ == '__main__':
    app.run(debug=True)
