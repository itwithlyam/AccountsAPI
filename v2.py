import mysql.connector  # todo: uncomment
from flask import jsonify, request

import os
import flask
import json

app = flask.Flask(__name__)

# todo: move config to config.py + core

assert True in [x in os.listdir() for x in ["administrators.json", "config.json"]], \
    "Please make sure the required config files are present in the same directory as the executable. "
# todo: back to false

config = json.loads(open("config.json", "r").read())

dbconfig = config["DATABASE"]  # todo: with

permissions = json.loads(open("administrators.json", "r").read())


def has_permissions(h_token, lvl):
    return True in [h_token == x["check"] for x in permissions.values() if x["level"] >= lvl]


@app.route('/', methods=['GET'])  # todo: better decorator (perm req, )
def home():
    auth = request.args.get("auth")
    if auth == None:
        return unauthorized(401)
    if has_permissions(h_token=auth, lvl=1) is False:
        return forbidden(403)

    return "OK"  # todo: online socket check / whois / perms


@app.route('/accounts', methods=['GET'])
def get_accounts():
    mydb = mysql.connector.connect(host=dbconfig["HOST"], user=dbconfig["USER"], password=dbconfig["PASSWORD"],
                               database=dbconfig["DATABASE"])
    query = request.args

    auth = query.get("auth")
    if auth == None:
        return unauthorized(401)
    if has_permissions(h_token=auth, lvl=2) is False:
        return forbidden(403)

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM accounts")
    myresult = mycursor.fetchall()
    print(myresult)

    accountData = "{"

    yes = False

    for account in myresult:
        id = account[1]
        accountData += f'"{id}":'
        data = account[0].replace('}', f',"id":"{id}"}}')
        accountData += data
        accountData += ","
        yes = True

    if yes: accountData = accountData[:-1]
    accountData += "}"

    response = flask.make_response(accountData)
    response.headers['Access-Control-Allow-Origin'] = '*'

    print(f"OUTPUTTED ACCOUNT")

    return response

@app.route('/accountsbyid', methods=['GET'])
def accounts_by_id():
    mydb = mysql.connector.connect(host=dbconfig["HOST"], user=dbconfig["USER"], password=dbconfig["PASSWORD"],
                            database=dbconfig["DATABASE"])
    args = request.args
    auth = args.get("auth")
    if auth == None:
        return unauthorized(401)
    if has_permissions(h_token=auth, lvl=2) is False:
        return forbidden(403)

    if 'id' in args:
        id = args.get("id")
    else:
        return badrequest(400)

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM accounts WHERE id={id}")
    myresult = mycursor.fetchall()

    accountData = "{"

    yes = False

    for account in myresult:
        id = account[1]
        accountData += f'"{id}":'
        data = account[0].replace('}', f',"id":"{id}"}}')
        accountData += data
        accountData += ","
        yes = True

    if yes: accountData = accountData[:-1]
    accountData += "}"

    response = flask.make_response(accountData)
    response.headers['Access-Control-Allow-Origin'] = '*'

    print(f"OUTPUTTED ACCOUNT {id}")

    return response


@app.route('/makeaccounts', methods=['POST', 'GET'])
def send_accounts():
    mydb = mysql.connector.connect(host=dbconfig["HOST"], user=dbconfig["USER"], password=dbconfig["PASSWORD"],
                               database=dbconfig["DATABASE"])
    query = request.headers
    gets = request.args
    auth = gets.get("auth")
    if auth == None:
        return unauthorized(401)
    if has_permissions(h_token=auth, lvl=3) is False:
        return forbidden(403)


    if 'username' in request.headers:
        username = query.get("username")
    else:
        return badrequest(400)
    if 'password' in request.headers:
        password = query.get("password")
    else:
        return badrequest(400)

    
    data = f'{{"username":"{username}","password":"{password}"}}'

    print(data)

    mycursor = mydb.cursor()
    mycursor.execute(f"INSERT INTO `accounts`(`data`) VALUES ('{data}')")
    mydb.commit()

    print(f"CREATED ACCOUNT {username}")

    return "<h1>204 Complete no content</h1><p>There is no content to be shown</p>"

@app.route('/deleteaccounts', methods=['GET', 'DELETE'])
def delete_accounts():
    mydb = mysql.connector.connect(host=dbconfig["HOST"], user=dbconfig["USER"], password=dbconfig["PASSWORD"],
                               database=dbconfig["DATABASE"])
    query = request.args
    auth = query.get("auth")
    if auth == None:
        return unauthorized(401)
    if has_permissions(h_token=auth, lvl=4) is False:
        return forbidden(403)
    

    if "id" in query:
        id = query.get("id")
    else:
        return badrequest(400)

    mycursor = mydb.cursor()
    mycursor.execute(f"DELETE FROM accounts WHERE id={id};")
    mydb.commit()

    print(f"DELETED ACCOUNT {id}")

    return "<h1>204 Complete no content</h1><p>There is no content to be shown</p>"

@app.route('/modifyaccounts', methods=['POST', 'GET', 'PATCH'])
def modify_accounts():
  mydb = mysql.connector.connect(host=dbconfig["HOST"], user=dbconfig["USER"], password=dbconfig["PASSWORD"],
                               database=dbconfig["DATABASE"])
  query = request.headers
  gets = request.args
  auth = gets.get("auth")
  if auth == None:
      return unauthorized(401)
  if has_permissions(h_token=auth, lvl=3) is False:
      return forbidden(403)


  if 'username' in request.headers:
      username = query.get("username")
  else:
      return badrequest(400)
  if 'password' in request.headers:
      password = query.get("password")
  else:
      return badrequest(400)
  if 'id' in request.headers:
      id = query.get("id")
  else:
      return badrequest(400)

  
  data = f"'{{\"username\":\"{username}\",\"password\":\"{password}\"}}'"

  print(data)

  mycursor = mydb.cursor()
  mycursor.execute(f'UPDATE accounts SET data={data} WHERE id={id};')
  mydb.commit()

  print(f"MODIFIED ACCOUNT {id}")

  return "<h1>204 Complete no content</h1><p>There is no content to be shown</p>"


@app.errorhandler(404)
def page_not_found(e):
    return '{ "code": "404" }', 404
@app.errorhandler(403)
def forbidden(e):
    return '{ "code": "403" }', 403
@app.errorhandler(400)
def badrequest(e):
    return '{ "code": "400" }', 400
@app.errorhandler(401)
def unauthorized(e):
    return '{ "code": "401" }', 401
@app.errorhandler(500)
def servererror(e):
    return '{ "code": "500" }', 500


if __name__ == "__main__": app.run()
