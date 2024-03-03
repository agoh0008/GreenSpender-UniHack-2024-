from flask import Flask
import boto3
app = Flask(__name__)


# API route
@app.route("/members")
def members():
    return {"members": ["member1", "member2", "member3", "member4"]}


if __name__ == "__main__":
    app.run(debug=True)
