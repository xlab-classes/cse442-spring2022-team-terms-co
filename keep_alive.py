from flask import Flask
from threading import Thread

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def main():
    return render_template("index.html")


def run():
    app.run(host="0.0.0.0", port=8888)


def keep_alive():
    server = Thread(target=run)
    server.start()
