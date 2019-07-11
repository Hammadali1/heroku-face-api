from flask import Flask, jsonify,json,request,render_template
app = Flask(__name__)

@app.route("/")
def index():
    return ("OKKKK")

if __name__ == "__main__":
    app.run(debug=True)
