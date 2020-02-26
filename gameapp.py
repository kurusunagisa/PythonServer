from flask import Flask, request
import pymysql
import key
import secrets
import string
import json

app = Flask(__name__)

connect = pymysql.connect(host='localhost', user='root',password=key.key, db='gamedb', autocommit=True, cursorclass=pymysql.cursors.DictCursor)

db = connect.cursor();

@app.url_value_preprocessor  # @app.routeが呼び出されたときに関数に入る前に呼び出されるメソッド
def GetUserData(endpoint, values):  # jsonデータを受け取って渡すだけ
  print(endpoint, values)
  # リクエストごとに処理を分ける
  if (endpoint == "UserCreateRequest"):
    data = request.get_data()  # request.dataだと自動で値が返らないらしい
    print(data)
    values["name"] = json.loads(data)
  elif (endpoint == "UserGetResponse"):
    values["token"] = request.headers.get("x-token")
  elif (endpoint == "UserUpdateRequest"):
    data = request.get_data()
    values["name"] = json.loads(data)
    values["token"] = request.headers.get("x-token")
  #values["token"] = json.loads(data)

@app.route('/user/create', methods=['POST',])
def UserCreateRequest(name):
  print(name)
  token = ''
  for _ in range(20):
    token += str(secrets.choice(string.ascii_letters))
  print(token)
  db.execute('INSERT INTO user (NAME, TOKEN) VALUES (%s,%s)',(name['token'],token))
  return UserCreateResponse(token)

def UserCreateResponse(token):
  return json.dumps({'token' : token})

@app.route('/user/get', methods=['GET'],)
def UserGetResponse(token):
  db.execute('SELECT NAME FROM user WHERE TOKEN=%s', (token)) #SQLの実行
  print("token : ", token)
  return db.fetchone() #SQLの出力をフェッチ

@app.route('/user/update', methods=['PUT'])
def UserUpdateRequest(name, token):
  print(name['name'] , token)
  db.execute('UPDATE user SET NAME=%s WHERE TOKEN=%s', (name['name'], token))
  return ""

if __name__ == '__main__':
  #token = UserCreateRequest('{"token": "名取さな"}')
  #print(token)
  #name = UserGetResponse("44f706f5e1c7e036356648fa01fd2e142399bdbc6cb269624331bad45616970cb8d23bca26df97b76062a0a109dd12bd8f201ae0b089a98d5a4075faee5d9a64")
  #print(name)
  app.run(host='localhost', port='8080', debug=True)
