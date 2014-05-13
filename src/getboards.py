# Author: Niti Verma
from bottle import get, post, request, run, response, Bottle # or route
import bottle
from uuid import uuid4
from bottle.ext import couchdb
import json

app = Bottle()
plugin = couchdb.Plugin('pinterest_db', server_name='http://localhost:5984')
app.install(plugin)

def is_logged_in(db, user_id):
  if db[user_id]:
    return True
  else:
    return False

#Login
@app.route('/v1/login', method='POST')
def login(db):
  username = request.json['username']
  password = request.json['password']
  map_fun = getMapFun('user')
  user_id = None
  for row in db.query(map_fun):
    user = row.value
    if user['username'] == username and user['password'] == password:
      user_id = row.key
      break
  if user_id:
    response.status = 200
    return {'user_id': user_id}
  else:
    abort(401, 'Invalid username or password')


#Get All Pins
@app.route('/v1/pins', method = 'GET')
def get_all_pins(db):
  map_fun = getMapFun('pin')
  pins = []
  for row in db.query(map_fun):
    pins.append({'pin_name': row.value['pin_name'], 'pin_url': row.value['pin_url']})
  response.set_header('Content-Type', 'application/json')
  return json.dumps(pins)

#Get All Boards
@app.route('/v1/boards')
def get_boards(db):
  try:
    map_fun = getMapFun('board')
    boards = []
    for row in db.query(map_fun):
      boards.append({
        'board_id': row.key, 
        'board_name': row.value
      })
    response.set_header('Content-Type', 'application/json')
    return json.dumps(boards)
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")

#Get board
@app.route('/v1/boards/:board_id')
def get_board(board_id, db):
  try:
    doc = db[board_id]
    pin_ids = doc['pins']
    map_fun = getMapFun('pin')
    pins = []
    for row in db.query(map_fun):
      if row.key in pin_ids:
        pins.append({
          'pin_name': row.value['pin_name'], 
          'pin_url': row.value['pin_url']
        })
    response.set_header('Content-Type', 'application/json')
    return json.dumps(pins)
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")

#Get a pin for pin_id
@app.route('/v1/pin/:pin_id', method = 'GET')
def get_pin(pin_id, db):
  pin = db[pin_id]
  result = {
    'pin_url': pin['pin_url'],
    'pin_name': pin['pin_name'],
    'comments': pin['comments']
  }
  return result

#Upload a Pin
@app.route('/v1/user/:user_id/pin/upload', method = 'POST')
def uploadpin(user_id, db):
  try:
    if not is_logged_in(db, user_id):
      abort(401, 'You have to login to create a pin.')
    doc_id = 'pin:' + uuid4().hex
    db[doc_id] = {
      'pin_name': request.json['pin_name'],
      'pin_url': request.json['pin_url'],
      'comments': []
    }
    response.status = 201
    return {'pin_id': doc_id}
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")

#Registration
@app.route('/v1/reg', method = 'POST')
def signup(db):
  username = request.json['username']
  password = request.json['password']
  name = request.json['name']
  doc_id = 'user:' + uuid4().hex
  db[doc_id] = {'username': username,"password":password,"name":name,"boards":[],"pins":[]}
  rsp = {}
  rsp["userid"] = doc_id
  return rsp

# adding a comment to a pin
@app.route('/v1/user/:user_id/pin/:pin_id', method = 'POST')
def add_comment(user_id, pin_id, db):
  try:
    if not is_logged_in(db, user_id):
      abort(401, 'You have to login to create a pin.')
    pin = db[pin_id]
    pin['comments'].append({
      'creator': user_id,
      'comment': request.json['comment']
    })
    db.save(pin)
    return {'pin_id': pin_id}
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")

#Create Board
@app.route('/v1/user/:user_id/board/', method='POST')
def create_board(user_id, db):
  try:
    print 'HAHAHA'
    if not is_logged_in(db, user_id):
      abort(401, 'You have to login to create a board.')
    print 'HAHAHA'

    doc_id = 'board:' + uuid4().hex
    db[doc_id] = {
      'name': 'board',#request.json['boardname'], 
      'owner': user_id, 
      'pins': []
    }
    print 'HAHAHA'

    response.status = 201
    return {'Token': doc_id}
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")

#Deleting a board
@app.route('/v1/user/:user_id/board/:board_id/', method='DELETE')
def delete_board(user_id, board_id, db):
  try:
    if not is_logged_in(db, user_id):
      abort(401, 'You have to login to delete a board.')
    board = db[board_id]
    if user_id!= board['owner']:
      abort(401, 'You do not have right to delete this board.')
    db.delete(board)
    response.status = 201
    return 'Board deleted.'
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")

# Map function collecting data for other functions
def getMapFun(field):
  return '''function(doc) {
      if (doc._id.indexOf('%s:') === 0) {
        emit(doc._id, doc);
      }
    }''' % (field)

# Attaching Pin to a board and user
@app.route('/v1/user/:user_id/board/:board_id', method='PUT')
def attach_pin(user_id, board_id, db):
  try:
    if not is_logged_in(db, user_id):
      abort(401, 'You have to login to attach a pin.')
    board= db[board_id]
    pin_id= request.json['pin_id']
    if pin_id in board['pins']:
      return 'Already Attached'
    else:
      board['pins'].append(pin_id)
      db.save(board)
      response.status = 201
      return 'Pin Attached!!'
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")



# Getting Boards of a user
@app.route('/v1/user/:user_id')
def get_user_boards(user_id, db):
  try:
    if not is_logged_in(db, user_id):
      abort(401, 'You have to login to view your boards.')
    user = db[user_id]
    map_fun = getMapFun('board')
    boards = []
    for row in db.query(map_fun):
      if row.key in user['boards']:
        boards.append({
          'board_id': row.key, 
          'board_name': row.value
        })
    return {'name': user['name'], 'boards': boards}
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")


if __name__ == "__main__":   
  run(app, host='localhost', port=8080, reloader=True, debug=True)
