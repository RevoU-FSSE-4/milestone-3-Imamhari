from flask import Blueprint, request
from connectors.mysql_connector import connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from models.user import User
from flask_login import login_user, logout_user, login_required

user_routes = Blueprint('user_routes', __name__)

#register
@user_routes.route('/register', methods=['POST'])
def register():
    Session = sessionmaker(connection)
    session = Session()

    session.begin()

    try:
        NewUser = User(
            username = request.form['username'],
            email = request.form['email'],
        )

        NewUser.set_password(request.form['password_hash'])

        session.add(NewUser)
        session.commit()

    except Exception as e:
        print(e)
        session.rollback()
        return {"message": "Failed to Register"}, 501
    
    return {"message": "Successfully Registered"}, 202

#login
@user_routes.route('/login', methods=['POST'])
def login():
    Session = sessionmaker(connection)
    session = Session()

    session.begin()

    try: 
        email = request.form['email']
        username = session.query(User).filter(User.email == email).first()

        if username is None:
            return {"message": "User does not exist"}, 401
        
        if not username.check_password(request.form['password_hash']):
            return {"message": "Invalid Password"}, 401
        
        login_user(username)

        session_id = request.cookies.get('session')

        return {
             
            "session_id": session_id,
            "message": "Successfully Logged In"
            }

    except Exception as e:
        print(e)
        session.rollback()
        return {"message": "Failed to Login"}, 501

    return {"message": "Successfully Logged In"}, 202
    

# get users
@user_routes.route('/users', methods=['GET'])
@login_required
def get_user():
    Session = sessionmaker(connection)
    session = Session()

    try:
        user_query = select(User)

        result = session.execute(user_query)
        users = []

        for row in result.scalars():
            users.append({
                "id": row.id,
                "username": row.username,
                "email": row.email,
                "created_at": row.created_at,
                "updated_at": row.updated_at
            })
            return {
                "users": users,
                "message": "Successfully Retrieved Users"
                }, 202
        
    except Exception as e:
        print(e)
        return {"message": "Failed to Get User"}, 501

    return {"message": "Successfully Retrieved User"}, 202


#update user
@user_routes.route('/users/<id>', methods=['PUT'])
@login_required
def update_user(id):
    Session = sessionmaker(connection)
    s = Session()
    s.begin()

    try:
        user = s.query(User).filter(User.id == id).first()
        user.username = request.form['username']
        user.email = request.form['email']

        s.commit()

    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Failed to Update User"}, 501

    return {"message": "Successfully Updated User"}, 202


#logout
@user_routes.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return {"message": "Successfully Logged Out"}, 202

