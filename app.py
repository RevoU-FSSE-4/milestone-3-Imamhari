from flask import Flask
from dotenv import load_dotenv

from flask_login import LoginManager

from models.user import User
from controllers.user import user_routes, s
from controllers.account import account_routes
from controllers.transaction import transaction_routes

import os


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(user_routes)
app.register_blueprint(account_routes)
app.register_blueprint(transaction_routes)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    
        return s.query(User).get(int(user_id))

@app.route("/")
def index():

    
    # Session = sessionmaker(connection)
    # with Session() as session:
    #     session.execute(text("INSERT INTO users (username, email, password_hash) VALUES ('john', 'john@example.com', '1234')"))
    #     session.commit()

    return "inserted successfully!" 



if __name__ == "__main__":
    app.run(debug=True)