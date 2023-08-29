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
    rows = cursor.execute("SELECT * FROM USERS WHERE email='{}' AND password='{}' LIMIT 1".format(email,password))
    user_response = {
        'username': '',
        'email': '',
        'id': 0
    }
    for user in rows:
        user_response["username"] = user[0]
        user_response["email"] = user[1]
        user_response["id"] = user[3]
    
    return user_response,200


@app.route('/createtask',methods=['POST'])
def create_task():
    if request.method == 'POST':
        model = request.get_json()
        user_id = ""
        name = ""
        content = ""
        try:
            user_id = model["id_user"]
            name = model["name"]
            content = model["content"]
            
            
        except:
            return Response("{'error':'Tarea no registrada'}",status=400,mimetype='application/json')
        connection = sqlite3.connect("maindb.db",check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO TASKS (user_id,NAME,CONTENT) VALUES ({},'{}','{}')".format(user_id,name,content))
        connection.commit()
        cursor.close()
        connection.close()
    
        return Response("{'status':'Tarea fue registrada'}",status=201, mimetype='application/json')
    

@app.route('/tasklist/<userid>')
def tasklist(userid=0):
    tasks = []
    connection = sqlite3.connect("maindb.db",check_same_thread=False)
    cursor = connection.cursor()
    rows = cursor.execute("SELECT * FROM TASKS WHERE user_id={}".format(userid))
    for task in rows:
        task = {
            'task_id': task[0],
            'name': task[2],
            'content': task[3]
        }
        tasks.append(task)
    connection.commit()
    cursor.close()
    connection.close()
    return tasks,200



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
            cursor.execute("INSERT INTO USERS (username,email,password) VALUES('{}','{}','{}')".format(username,email,password))
            connection.commit()
            cursor.close()
            connection.close()
        except:
            return Response("{'error':'Usuario no registrado'}",status=400,mimetype='application/json')
        
        

        return Response("{'status':'El usuario fue registrado'}",status=201, mimetype='application/json')