from flask import Blueprint, request
from sqlalchemy import select
from models.transaction import Transaction
from controllers.user import s


transaction_routes = Blueprint('transaction_routes', __name__)


#create transaction
@transaction_routes.route('/transactions', methods=['POST'])
def create_transaction():
    

    s.begin()

    try:
        NewTransaction = Transaction(  
            from_account_id = request.form['from_account_id'],
            to_account_id = request.form['to_account_id'],
            amount = request.form['amount'],
            type = request.form['type'],
            description = request.form['description'],
        )

        s.add(NewTransaction)
        s.commit()
    
    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Failed to Create Transaction"}, 501

    return {"message": "Successfully Created Transaction"}, 202


#view transaction
@transaction_routes.route('/transactions', methods=['GET'])
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
