import json
import falcon
from tinydb import TinyDB
from uuid import uuid4 as uuid

class Entities:
  def __init__(self, db_path):
    self.__db = TinyDB(db_path)

  def on_get(self, req, resp):
    doc = self.__db.all()
    resp.text = json.dumps(doc, ensure_ascii=False)
    resp.status = falcon.HTTP_200
    resp.content_type = falcon.MEDIA_JSON

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
