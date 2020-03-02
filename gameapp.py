from flask import Flask, request, jsonify
import pymysql
import key
import secrets
import string
import json

# TODO : エラー処理(どうやるんだ)

app = Flask(__name__)

connect = pymysql.connect(host='localhost', user='root', password='',
                          db='gamedb', autocommit=True, cursorclass=pymysql.cursors.DictCursor)

db = connect.cursor()


@app.url_value_preprocessor  # @app.routeが呼び出されたときに関数に入る前に呼び出されるメソッド パス変数を作ってるっぽい？
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
    elif (endpoint == "GachaDrawRequest"):
        values["token"] = request.headers.get("x-token")
        data = request.get_data()
        values["times"] = json.loads(data)
    #values["token"] = json.loads(data)


@app.route('/user/create', methods=['POST', ])
def UserCreateRequest(name):
    print(name)
    token = ''
    for _ in range(20):
        token += str(secrets.choice(string.ascii_letters))
    print(token)
    db.execute('INSERT INTO users (name, token) VALUES (%s,%s)',
               (name['token'], token))
    return UserCreateResponse(token)


def UserCreateResponse(token):
    return json.dumps({'token': token})


@app.route('/user/get', methods=['GET'],)
def UserGetResponse(token):
    db.execute('SELECT name FROM users WHERE token=%s', (token))  # SQLの実行
    print("token : ", token)
    print(db.fetchone)
    return jsonify(db.fetchone())  # SQLの出力をフェッチ


@app.route('/user/update', methods=['PUT'])
def UserUpdateRequest(name, token):
    print(name['name'], token)
    db.execute('UPDATE users SET name=%s WHERE name=%s', (name['name'], token))
    return ""


@app.route('/gacha/draw', methods=['POST'])
def GachaDrawRequest(token, times):
    print(token, times['times'])
    #result = []
    #for _ in range(times['times']):
        #result.append(GachaDrawResponse())
        #print(result)
    #return result
    return jsonify(GachaDrawResponse())


def GachaDrawResponse():
    return GachaResult()


def GachaResult():
    star = []
    rand = secrets.randbelow(100)
    if (rand < 5):
        rare = 3
    elif (rand < 20):
        rare = 2
    else:
        rare = 1
    db.execute('WITH CTE AS (SELECT * FROM chars_rare WHERE rare=%s) SELECT * FROM CTE ORDER BY RAND() LIMIT 1', rare)  # SQLの実行
    print(db.fetchone)
    return db.fetchone


if __name__ == '__main__':
    #token = UserCreateRequest('{"token": "名取さな"}')
    # print(token)
    #result = GachaResult()
    #print(GachaResult())
    #name = UserGetResponse("44f706f5e1c7e036356648fa01fd2e142399bdbc6cb269624331bad45616970cb8d23bca26df97b76062a0a109dd12bd8f201ae0b089a98d5a4075faee5d9a64")
    # print(name)
    app.run(host='localhost', port='8080', debug=True)
