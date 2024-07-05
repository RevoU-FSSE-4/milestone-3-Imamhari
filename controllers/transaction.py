from flask import Blueprint, request
from sqlalchemy import select
from models.transaction import Transaction
from models.account import Account
from controllers.user import s
from flask_login import login_required


transaction_routes = Blueprint('transaction_routes', __name__)


#create transaction
@transaction_routes.route('/transactions', methods=['POST'])
@login_required
def create_transaction():
    

    try:
        NewTransaction = Transaction(  
            from_account_id = request.form['from_account_id'],
            to_account_id = request.form['to_account_id'],
            amount = request.form['amount'],
            type = request.form['type'],
            description = request.form['description'],
        )


        if request.form['type'] == 'transfer':
            account_to = s.query(Account).filter(Account.id == request.form['to_account_id']).first()
            account_from = s.query(Account).filter(Account.id == request.form['from_account_id']).first()
            # print('account', account)
            account_from.balance = int(account_from.balance) - int(NewTransaction.amount)
            account_to.balance = int(account_to.balance) + int(NewTransaction.amount)
            s.add(account_to)
            s.add(account_from)

        elif request.form['type'] == 'withdraw':
            account = s.query(Account).filter(Account.id == request.form['to_account_id']).first()
            print('account', account)
            account.balance = int(account.balance) - int(NewTransaction.amount)
            s.add(account)

        elif request.form['type'] == 'deposit':
            account = s.query(Account).filter(Account.id == request.form['to_account_id']).first()
            print('account', account)
            account.balance = int(account.balance) + int(NewTransaction.amount)
            s.add(account)

        s.add(NewTransaction)
        s.commit()
    
    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Failed to Create Transaction"}, 501

    return {"message": "Successfully Created Transaction"}, 202


#view transaction
@transaction_routes.route('/transactions', methods=['GET'])
@login_required
def get_transaction():
    # Session = sessionmaker(connection)
    # s = Session()

    try:
        transaction_query = select(Transaction)

        result = s.execute(transaction_query)
        transactions = []

        for row in result.scalars():
            transactions.append({
                "id": row.id,
                "from_account_id": row.from_account_id,
                "to_account_id": row.to_account_id,
                "amount": row.amount,
                "type": row.type,
                "description": row.description,
                "created_at": row.created_at
            })

        return {
            "transactions": transactions,
            "message": "Successfully Retrieved Transactions"
        }
    
    except Exception as e:
       
        return {"message": "Failed to Get Transaction"}, 501

    return {"message": "Successfully Retrieved Transaction"}, 202


#view transaction by id
@transaction_routes.route('/transactions/<id>', methods=['GET'])
@login_required
def get_transaction_by_id(id):
    # Session = sessionmaker(connection)
    # s = Session()

    try:
        transaction_query = select(Transaction).where(Transaction.id == id)

        result = s.execute(transaction_query)
        transaction = []

        for row in result.scalars():
            transaction.append({
                "id": row.id,
                "from_account_id": row.from_account_id,
                "to_account_id": row.to_account_id,
                "amount": row.amount,
                "type": row.type,
                "description": row.description,
                "created_at": row.created_at
            })

        return {
            "transaction": transaction,
            "message": "Successfully Retrieved Transaction by Id"
        }
    
    except Exception as e:
       
        return {"message": "Failed to Get Transaction"}, 501

    return {"message": "Successfully Retrieved Transaction"}, 202
