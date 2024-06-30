from flask import Flask, jsonify, request # pip3 install flask
from pymongo import MongoClient # pip3 install pymongo
from bson import ObjectId # bson included in the pymongo

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection
client = MongoClient("ReplaceThisWithYourDatabaseUri") #the link will be replace by your mongodb database URI
db = client['yourDatabaseNameHere'] #pythonTodo will be replace by Database name
collection = db['collectionNameHere'] #todo will be replace by Collection name here

# example.com/todos
# Create a new TODO
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if 'title' not in data or 'status' not in data :
        return jsonify({'error': 'Missing required fields'}), 400

    todo = {
        'title': data['title'],
        'status': data['status'],
        'description': data.get('description', '')
    }
    result = collection.insert_one(todo)
    if result.inserted_id:
        return jsonify({'message': 'Todo created successfully', 'id': str(result.inserted_id)}), 201
    else:
        return jsonify({'error': 'Failed to create todo'}), 500


# Update TODO by ID
# example.com/update/id
@app.route('/update/<string:todo_id>', methods=['POST'])
def update_todo(todo_id):
    todo_obj_id = ObjectId(todo_id)
    data = request.get_json()
    updated_todo = {
        'title': data.get('title', ''),
        'status': data.get('status', ''),
        'description': data.get('description', '')
    }
    result = collection.update_one({'_id': todo_obj_id}, {'$set': updated_todo})
    if result.modified_count > 0:
        return jsonify({'message': 'Todo updated successfully'})
    else:
        return jsonify({'error': 'Todo not found'}), 404
    

# List all TODOs
# example.com/todos
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = list(collection.find({}))
    # Convert ObjectId to string for each document
    for todo in todos:
        todo['_id'] = str(todo['_id'])
    return jsonify({'todos': todos})


# Getting specific ToDo
# example.com/get/id
@app.route('/get/<string:todo_id>', methods=['GET'])
def get_todo(todo_id):
    try:
        # Convert todo_id from string to ObjectId
        todo_obj_id = ObjectId(todo_id)
        todo = collection.find_one({'_id': todo_obj_id})
        if todo:
            todo['_id'] = str(todo['_id'])
            return jsonify({'todo': todo})
        else:
            return jsonify({'error': 'Todo not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Invalid todo_id format: {str(e)}'}), 400
    
    
# Delete TODO by ID
# example.com/delete/id
@app.route('/delete/<string:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo_obj_id = ObjectId(todo_id)
    result = collection.delete_one({'_id': todo_obj_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Todo deleted successfully'})
    else:
        return jsonify({'error': 'Todo not found'}), 404


# Run the application
if __name__ == '__main__':
    app.run(debug=True)