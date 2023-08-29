from flask import Flask, request, redirect, url_for,Response
import sqlite3

app = Flask(__name__)


@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/listusers")
def listUsers():
    connection = sqlite3.connect("maindb.db",check_same_thread=False)
    cursor = connection.cursor()
    rows = cursor.execute("SELECT * FROM USERS")
    response = []
    for user in rows:
        model = {}
        model['username'] = user[0]
        model['email'] = user[1]
        response.append(model)
    cursor.close()
    connection.close()
    return response,200
    

@app.route("/login", methods=['POST'])
def login():
    model = request.get_json()
    email = model["email"]
    password = model["password"]
    connection = sqlite3.connect("maindb.db",check_same_thread=False)
    cursor = connection.cursor()
    rows = cursor.execute("SELECT * FROM USERS WHERE email='{}' AND password='{}'".format(email,password))
    if(len(list(rows)) != 1):
        return "{'error':'Usuario no encontrado'}",404
    
    return model,200




@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        email = ""
        password = ""
        username = ""
        model = request.get_json()
        try:
            email = model["email"]
            password = model["password"]
            username = model["username"]
            connection = sqlite3.connect("maindb.db",check_same_thread=False)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO USERS VALUES('{}','{}','{}')".format(username,email,password))
            connection.commit()
            cursor.close()
            connection.close()
        except:
            return Response("{'error':'Usuario no registrado'}",status=400,mimetype='application/json')
        
        

        return Response("{'status':'El usuario fue registrado'}",status=201, mimetype='application/json')