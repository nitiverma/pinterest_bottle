# Author: Niti Verma
from bottle import get, post, request, run, response, Bottle # or route
import bottle
from bottle.ext import couchdb

app = Bottle()
#Bottle.debug(True)

plugin = couchdb.Plugin('pinterest_db', server_name='http://localhost:5984')
app.install(plugin)

@app.route('/v1/boards')
def get_boards(db):
  try:
    map_fun = '''function(doc) {
      emit(doc._id, doc.name);
    }'''
    boards = []
    for row in db.query(map_fun):
      boards.append({'board_id': row.key, 'board_name': row.value})
    return {'boards': boards}
  except couchdb.ResourceNotFound:
    return bottle.HTTPError(404, "Page not found")



run(app, host='localhost', port=8080, reloader=True, debug=True)
