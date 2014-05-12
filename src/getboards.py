# Author: Niti Verma
from bottle import get, post, request, run, response, Bottle # or route
import bottle
from uuid import uuid4
from bottle.ext import couchdb

app = Bottle()
#Bottle.debug(True)

plugin = couchdb.Plugin('pinterest_db', server_name='http://localhost:5984')
app.install(plugin)

def is_logged_in():
  return True

@app.route('/v1/user/:user_id/board/', method='POST')
def create_board(user_id, db):
  try:
    if not is_logged_in():
      abort(401, 'You have to login to create a board.')
    doc_id = 'board:' + uuid4().hex
    db[doc_id] = {'name': request.json['boardname'], 'owner': user_id}
    response.status = 201
    return 'Token: '+ doc_id
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")

@app.route('/v1/user/:user_id/board/:board_id/', method='DELETE')
def delete_board(user_id, board_id, db):
  try:
    if not is_logged_in():
      abort(401, 'You have to login to delete a board.')
    board = db[board_id]
    if user_id!= board['owner']:
      abort(401, 'You do not have right to delete this board.')
    db.delete(board)
    response.status = 201
    return 'Board deleted.'
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")


def getMapFun(field):
  return '''function(doc) {
      if (doc._id.indexOf('%s:') === 0) {
        emit(doc._id, doc.name);
      }
    }''' % (field)

@app.route('/v1/boards/:board_id')
def get_board(board_id, db):
  try:
    doc = db[board_id]
    pin_ids = doc['pins']
    map_fun = '''function(doc) {
      if (doc._id.indexOf('pins:') === 0) {
        emit(doc._id, doc);
      }
    }'''
    pins = []
    for row in db.query(map_fun):
      if row.key in pin_ids:
        pins.append({'pin_name': row.value['pin_name'], 'pin_url': row.value['pin_url']})
    return {'pins': pins}
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")

@app.route('/v1/boards')
def get_boards(db):
  try:
    map_fun = getMapFun('board')
    boards = []
    for row in db.query(map_fun):
      boards.append({'board_id': row.key, 'board_name': row.value})
    return {'boards': boards}
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")

@app.route('/v1/user/:user_id')
def get_user_boards(user_id, db):
  try:
    if not is_logged_in():
      abort(401, 'You have to login to view your boards.')
    user = db[user_id]
    map_fun = getMapFun('board')
    boards = []
    for row in db.query(map_fun):
      if row.key in user['boards']:
        boards.append({'board_id': row.key, 'board_name': row.value})
    return {'name': user['name'], 'boards': boards}
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")



run(app, host='localhost', port=8080, reloader=True, debug=True)
