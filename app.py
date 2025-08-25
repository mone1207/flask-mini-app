from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Flask!"

@app.route("/about")
def about():
    return "これはAboutページです"

# test

if __name__ == "__main__":
    app.run(debug=True)