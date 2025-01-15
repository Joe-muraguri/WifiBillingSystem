from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('dashboard.html')


import os
# Get the port from the environment variable or default to 5000
port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)