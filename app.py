from flask import Flask
from dotenv import load_dotenv
from connectors.mysql_connector import connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route("/")
def index():

     # insert data to product table
    Session = sessionmaker(connection)
    with Session() as session:
        session.execute(text("INSERT INTO users (username, email, password_hash) VALUES ('imam', 'qSf9C@example.com', '1234')"))
        session.commit()

    return "inserted successfully!" 



if __name__ == "__main__":
    app.run(debug=True)