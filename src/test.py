from webtest import TestApp
import getboards

def testCreateBoard():
  testapp = TestApp(getboards.app, {'port': '8080', 'reloader':'True', 'debug':'True'})

  response = testapp.post_json('/v1/user/user:1/board/', {'boardname': 'testBoard'})
  assert response.status == '201'
  print response

testCreateBoard()

# def test_functional_login_logout():
#     app = TestApp(mywebapp.app)

#     app.post('/login', {'user': 'foo', 'pass': 'bar'}) # log in and get a cookie

#     assert app.get('/admin').status == '200 OK'        # fetch a page successfully

#     app.get('/logout')                                 # log out
#     app.reset()                                        # drop the cookie

#     # fetch the same page, unsuccessfully
#     assert app.get('/admin').status == '401 Unauthorized'
