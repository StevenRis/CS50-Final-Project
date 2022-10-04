from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello"


# enable debug mode - no need to restart the server to refresh the page
# python app.py - run the server
if __name__ == '__main__':
    app.run(debug=True)