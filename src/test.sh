# Registration
curl -i -H "Content-Type: application/json" -X POST http://localhost:8080/v1/reg --data '{"username":"Jason", "name": "Jason Borne", "password":"abc"}' 

# # Get all pins
curl -i -H "Content-Type: application/json" -H "Accept: application/json" -X GET http://localhost:8080/v1/pins

# #Get All boards :

curl -i -H "Accept: application/json" -X GET http://localhost:8080/v1/boards

# #Get Board :

curl -i -H "Accept: application/json" -X GET http://localhost:8080/v1/boards/"board:8dce03f3e4c1447fb43279986c5ee8d1"

# #Get pin :

curl -i -H "Accept: application/json" -X GET http://localhost:8080/v1/pin/pin:1


# #Login :

curl -i -H "Content-Type: application/json" --data '{"username":"Jason", "password":"abc"}' -X POST http://localhost:8080/v1/login

# #Get user info / boards :

curl -i -H "Accept: application/json" -X GET http://localhost:8080/v1/user/"user:08e462f75ddf45928a21b36b331bc1e4" 

# #upload pin

curl -i -H "Content-Type: application/json" --data '{"pin_name":"different", "client_url":"www.google.com"}' -X POST http://localhost:8080/v1/user/"user:08e462f75ddf45928a21b36b331bc1e4"/pin/upload

# #create board :

curl -i -H "Accept: application/json" --data "boardName='www.google.com'" -X POST http://localhost:8080/v1/user/:user_id/board
  
# #Attach pin :

curl -i -H "Content-Type: application/json" --data '{"pin_id":"pin:9d0a67eb307d4f5db0dbca245837896c"}' -X PUT http://localhost:8080/v1/user/"user:08e462f75ddf45928a21b36b331bc1e4"/board/"board:8dce03f3e4c1447fb43279986c5ee8d1"

# #Delete Board :
curl -i -H "Accept: application/json" -X DELETE http://localhost:8080/v1/user/"user:08e462f75ddf45928a21b36b331bc1e4"/board/"board:8dce03f3e4c1447fb43279986c5ee8d1"

# #Add comment :
curl -i -H "Accept: application/json" --data {"comments":"www.google.com"} -X POST http://localhost:8080/v1/user/user:1/pin/pin:6a8c940ccdf94ed1aa06abd247a87b01


curl -i -H "Accept: application/json" -X GET http://localhost:8080/v1/pins





