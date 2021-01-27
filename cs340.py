from app import app, db
from app.models import Mutual_funds, Stocks, User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Mutual_funds': Mutual_funds, 'Stocks': Stocks}