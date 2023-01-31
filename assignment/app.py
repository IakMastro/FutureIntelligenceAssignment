import falcon
import os

from wsgiref.simple_server import make_server
from entities import Entities
from entity import Entity

# Environment variables
PORT = int(os.environ.get("PORT"))
DB = os.environ.get("DB")

# Application initialization
app = application = falcon.App()

# Routes
app.add_route("/entities", Entities(DB))
app.add_route("/entities/{_id}", Entity(DB))

if __name__ == '__main__':
  with make_server('0.0.0.0', PORT, app) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()
