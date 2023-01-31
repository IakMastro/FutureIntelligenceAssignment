import json
import falcon
from tinydb import TinyDB, Query

class Entity:
  def __init__(self, db_path):
    self.__db = TinyDB(db_path)
    self.__Entity = Query()

  def on_get(self, req, resp, _id):
    entity = self.__db.search(self.__Entity.id == _id)
    if len(entity) > 0:
      resp.text = json.dumps(entity[0], ensure_ascii=False)
      resp.status = falcon.HTTP_200
      resp.content_type = falcon.MEDIA_JSON
    else:
      resp.text = "No entity found with this ID"
      resp.status = falcon.HTTP_404
      resp.content_type = falcon.MEDIA_TEXT

  def on_put(self, req, resp, _id):
    raw_data = json.load(req.bounded_stream)
    entity = self.__db.search(self.__Entity.id == _id)
    if len(entity) > 0:
      self.__db.update(raw_data, self.__Entity.id == _id)
      resp.text = "Entity updated"
      resp.status = falcon.HTTP_200
      resp.content_type = falcon.MEDIA_TEXT
    else:
      resp.text = "No entity found with this ID"
      resp.status = falcon.HTTP_404
      resp.content_type = falcon.MEDIA_TEXT

  def on_delete(self, req, resp, _id):
    entity = self.__db.search(self.__Entity.id == _id)
    if len(entity) > 0:
      self.__db.remove(self.__Entity.id == _id)
      resp.text = "Entity deleted"
      resp.status = falcon.HTTP_200
      resp.content_type = falcon.MEDIA_TEXT
    else:
      resp.text = "No entity found with this ID"
      resp.status = falcon.HTTP_404
      resp.content_type = falcon.MEDIA_TEXT