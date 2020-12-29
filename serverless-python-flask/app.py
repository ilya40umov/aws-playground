from flask import Flask
app = Flask(__name__)

@app.route('/hello/<name>')
def hello(name: str) -> str:
    return f"Hello {name}!"
