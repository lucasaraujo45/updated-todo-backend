"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Todos

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/todo', methods=['POST','GET'])
def handle_todo():
    #GET
    if request == "GET":
        todo = Todos.query.all(todo_id)
        todoList = list(map(lambda x: x.serialize(), todo))
        return jsonify(todo.serialize()), 200
    #POST
    if request.method == "POST":
        body = request.get_json()

        todo = Todos(text=body['text'])
        db.session.add(todo)
        db.session.commit()

        response_body = {
            "status": "Successfully added.",
            "todo": todo.serialize(),
            "repr": repr(todo)
        }

        return jsonify(response_body), 205
return "Invalid Method", 404
@app.route('/todolist/<int:todo_id>', methods=['PUT', 'DELETE'])
def get_single_todo(todo_id):
    #PUT        
    if request.method == 'PUT':
        body = request.get_json()

        todo = Todos.query.get(todo_id)
        if "text" in body:
            Todo.text = body["text"]
        db.session.commit()

        return jsonify(todo.serialize()), 200

    #DELETE
    if request.method == 'DELETE':
        todo = Todos.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return "ok", 200
    return "Invalid Method", 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)