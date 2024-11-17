from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")

def flask_test_results():
    return render_template('report.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
