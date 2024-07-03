from flask import Blueprint, request
from sqlalchemy import select
from models.account import Account
from controllers.user import s

account_routes = Blueprint('account_routes', __name__)


#create account
@account_routes.route('/accounts', methods=['POST'])
def create_account():
    
    s.begin()

    try:
        NewAccount = Account(
            user_id = request.form['user_id'],
            account_type = request.form['account_type'],
            account_number = request.form['account_number'],
            balance = request.form['balance'],
        )

        s.add(NewAccount)
        s.commit()

    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Failed to Create Account"}, 501

    return {"message": "Successfully Created Account"}, 202

#update account
@account_routes.route('/accounts/<id>', methods=['PUT'])
def update_account(id):
    # Session = sessionmaker(connection)
    # s = Session()

    s.begin()

    try:
        account = s.query(Account).filter(Account.id == id).first()
        account.user_id = request.form['user_id']
        account.account_type = request.form['account_type']
        account.account_number = request.form['account_number']
        account.balance = request.form['balance']

        s.commit()

    except Exception as e:
        
        s.rollback()
        return {"message": "Failed to Update Account"}, 501

    return {"message": "Successfully Updated Account"}, 202


#get account
@account_routes.route('/accounts', methods=['GET'])
def get_account():
    # Session = sessionmaker(connection)
    # s = Session()

    try:
        account_query = select(Account)

        result = s.execute(account_query)

        accounts = []

        for row in result.scalars():
            accounts.append({
                "id": row.id,
                "user_id": row.user_id,
                "account_type": row.account_type,
                "account_number": row.account_number,
                "balance": row.balance,
                "created_at": row.created_at,
                "updated_at": row.updated_at
            })
    
        return {
            "message": "Successfully Retrieved Account",
            "accounts": accounts
            
        }, 202
    
    except Exception as e:
        print(e)
        return {"message": "Failed to Get Account"}, 501

    return {"message": "Successfully Retrieved Account"}, 202


#get account by id
@account_routes.route('/accounts/<id>', methods=['GET'])
def get_account_by_id(id):
    # Session = sessionmaker(connection)
    # s = Session()

    try:
        account_query = select(Account).where(Account.id == id)

        result = s.execute(account_query)
        account = []

        for row in result.scalars():
            account.append({
                "id": row.id,
                "user_id": row.user_id,
                "account_type": row.account_type,
                "account_number": row.account_number,
                "balance": row.balance,
                "created_at": row.created_at,
                "updated_at": row.updated_at
            })
            return {
                "message": "Successfully Retrieved Account by Id",
                "account": account}
    
    except Exception as e:
        print(e)
        return {"message": "Failed to Get Account"}, 501

    return {"message": "Successfully Retrieved Account"}, 202


#delete account
@account_routes.route('/accounts/<id>', methods=['DELETE'])
def delete_account(id):
    # Session = sessionmaker(connection)
    # s = Session()

    s.begin()

    try:
        account = s.query(Account).filter(Account.id == id).first()
        s.delete(account)
        s.commit()

    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Failed to Delete Account"}, 501

    return {"message": "Successfully Deleted Account"}, 202