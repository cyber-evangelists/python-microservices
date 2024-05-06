from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User
import re

app = Flask(__name__)

# Configure SQLAlchemy
engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


# Helper function to serialize User objects
def serialize_user(user):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }
# Validate email format
def is_valid_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True

# POST /users: Create a new user
@app.route('/users', methods=['POST'])
def create_user():
   
    data = request.json
    if 'name' not in data or not data['name'].strip():
        return jsonify(message='Name is required'), 400
    if 'email' not in data or not data['email'].strip():
        return jsonify(message='Email is required'), 400

    name = data['name']
    email = data['email']

    if not is_valid_email(email):
        return jsonify(message='Invalid email format'), 400

    session = DBSession()
    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()
    session.close()
    return jsonify(message='User created successfully'), 201

# GET /users: List all users
@app.route('/users', methods=['GET'])
def get_all_users():
    session = DBSession()
    users = session.query(User).all()
    session.close()
    serialized_users = [serialize_user(user) for user in users]
    return jsonify(users=serialized_users)


# GET /users/<id>: Retrieve a specific user by their ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    if user:
        return jsonify(serialize_user(user))
    else:
        return jsonify(message='User not found'), 404


# PUT /users/<id>: Update a user's information
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        session.close()
        return jsonify(message='User not found'), 404
    data = request.json
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'name' not in data or not data['name'].strip():
            return jsonify(message='Name is required'), 400
    if 'email' not in data or not data['email'].strip():
        return jsonify(message='Email is required'), 400
    if not is_valid_email(user.email):
            return jsonify(message='Invalid email format'), 400
    session.commit()
    session.close()
    return jsonify(message='User updated successfully')


# DELETE /users/<id>: Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        session.close()
        return jsonify(message='User not found'), 404
    session.delete(user)
    session.commit()
    session.close()
    return jsonify(message='User deleted successfully')


if __name__ == '__main__':
    app.run(debug=True)
