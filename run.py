import os

from app import create_app, db, cli
from app.models import User, Post, Notification, Message, Employee

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Employee': Employee, 'Message': Message,
            'Notification': Notification}
if __name__ == '__main__':
    app.run(debug=True)
