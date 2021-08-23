# import dependencies
from flask import Flask, jsonify

# create app instance
app = Flask(__name__)

# create index route
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
            f"one"
        )


# run in debug mode
if __name__ == "__main__":
    app.run(debug=True)