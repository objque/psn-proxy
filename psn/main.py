import json

from flask import Flask

from valkyrie import ValkyrieAPIClient

app = Flask(__name__)
client = ValkyrieAPIClient()


@app.route("/resolve/<id>")
def show(id):
    return json.dumps(client.resolve(id=id))


def create_app(*args, **kwargs):
    return app


if __name__ == '__main__':
    app.run("localhost", 8080)
