# Assignment for Future Intelligence

## Overview

As part of this assignment, a simple CRUD application was created using the Falcon web framework and TinyDB as the data storage. The application allows users to perform CRUD operations on a simple resource. Each entity have the following attributes: `id`, `name` and `type`. It is containerized with Docker.

## Stack

- Python 3.10
- Falcon Web Framework
- TinyDB
- Docker

## Initialization

Following the official documentation for both the [Falcon Framework](https://falcon.readthedocs.io/en/stable/) and [TinyDB](https://tinydb.readthedocs.io/en/latest/), the project was initialized using WSGI.

### Structure

```text
.
| .git
| .gitignore
| Dockerfile
| LICENSE
| requirements.txt
| run.sh
└-- assignment
    | __init__.py
    | app.py
    | entities.py
    | entity.py
```

### Configuration

On file `app.py`, the configuration of the application is being made.

Using `os.environ` to read the content, it reads two environment variables:

- `PORT`: The port of the application.
- `DB`: The name of the file that the DB will be saved at.

```py
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
```

`Entity` and `Entities` are two classes where the endpoints are defined.

### Challenges

#### Validate for entity creation fields

The validate for the entity creation was one of the challenges for this project.

The way it's solved is by trying to access the raw data's name or type fields.

If the field is missing from the request, Python automatically throws a `KeyError` exception.

Putting this in a try block, only valid entities are saved on the database.

```py
def on_post(self, req, resp):
  raw_data = json.load(req.bounded_stream)

  try:
    entity = {
      'id': str(uuid()),
      'name': raw_data['name'],
      'type': raw_data['type']
    }
    self.__db.insert(entity)
    resp.text = "Entity added to the database successfully!"
    resp.status = falcon.HTTP_201
    resp.content_type = falcon.MEDIA_TEXT

  except KeyError:
    resp.text = "Fields name and type are required"
    resp.status = falcon.HTTP_400
    resp.content_type = falcon.MEDIA_TEXT
```

## How to run

There is an automated script that builds the container and then it runs it.

Run `./run.sh` and check if it works with `curl localhost:8000`. It should return an empty array.
