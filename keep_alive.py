from flask import Flask
from threading import Thread
from flask import render_template

app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")

def run():
   app.run(host='0.0.0.0', port=8089, debug=True)


def keep_alive():
    server = Thread(target=run)
    server.start()
