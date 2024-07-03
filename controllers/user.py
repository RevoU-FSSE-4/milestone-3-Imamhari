from flask import Blueprint, request
from connectors.mysql_connector import connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from datetime import datetime

from models.user import User
from flask_login import login_user, logout_user, login_required, current_user

user_routes = Blueprint('user_routes', __name__)

Session = sessionmaker(connection)
s = Session()

#register
@user_routes.route('/register', methods=['POST'])
def register():
    
    s.begin()

    try:
        NewUser = User(
            username = request.form['username'],
            email = request.form['email'],
        )

        NewUser.set_password(request.form['password_hash'])

        s.add(NewUser)
        s.commit()

    except Exception as e:
        # print(e)
        s.rollback()
        return {"message": "Failed to Register"}, 501
    
    return {"message": "Successfully Registered"}, 202

#login
@user_routes.route('/login', methods=['POST'])
def login():
    # Session = sessionmaker(connection)
    # session = Session()
    s.begin()

    try: 
        email = request.form['email']
        username = s.query(User).filter(User.email == email).first()

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
        s.rollback()
        return {"message": "Failed to Login"}, 501

    return {"message": "Successfully Logged In"}, 202
    

# get users
@user_routes.route('/users/me', methods=['GET'])
@login_required
def get_user():
    # Session = sessionmaker(connection)
    # session = Session()

    try:
        user_query = select(User)

        result = s.execute(user_query)
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
                
            "message": "Successfully Retrieved Users",
            "users": users
        }, 202
        
    except Exception as e:
        print(e)
        return {"message": "Failed to Get User"}, 501

    return {"message": "Successfully Retrieved User"}, 202


#update user
@user_routes.route('/users/me', methods=['PUT'])
@login_required
def update_user():
    # Session = sessionmaker(connection)
    # s = Session()

    # s.begin()

    try:
        user = s.query(User).filter(User.id == current_user.id ).first()

        if "username" in request.form:
            user.username = request.form['username']
        if "email" in request.form:
            user.email = request.form['email']

        user.updated_at = datetime.now()

        s.commit()

    except Exception as e:
        # print(e)
        s.rollback()
        return {"message": "Failed to Update User"}, 501

    return {"message": "Successfully Updated User"}, 202


#logout
@user_routes.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return {"message": "Successfully Logged Out"}, 202

