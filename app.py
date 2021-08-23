# import dependencies
from Flask import Flask, jsonify

# create app instance
app = Flask(__name__)

# create index route
@app.route("/")
def home():
    return ("The possible routes are:\none")


# run in debug mode
if __name__ = "__main__":
    app.run(debug=True)