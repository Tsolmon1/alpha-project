from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login_manager
from app.search import add_to_index, remove_from_index, query_index
from flask import url_for
import json
from time import time

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128)) 
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)


    last_message_read_time = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='employee',
                                    lazy='dynamic')


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    


    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)
    
    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), employee=self)
        db.session.add(n)
        return n

# Set up user_loader
@login_manager.user_loader
def load_user(employee_id):
    return Employee.query.get(int(employee_id))

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class User(SearchableMixin, db.Model, UserMixin):
    __searchable__ = ['full_name']
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    full_name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    register_number = db.Column(db.String(50), unique=True)
    phone_number = db.Column(db.Integer, unique=True)
    civil_number = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80))
    address = db.Column(db.String(120))
    secure_question = db.Column(db.String(120))
    relate_phone = db.Column(db.Integer, unique=True)
    married = db.Column(db.Boolean)
    withlive = db.Column(db.String(80))
    home_income = db.Column(db.Integer)
    home_member_income = db.Column(db.Integer)
    educational_level = db.Column(db.String(80))
    is_job = db.Column(db.Boolean)
    company_name = db.Column(db.String(80))
    social_insurance = db.Column(db.Boolean)
    this_company_worked_year = db.Column(db.Integer)
    worked_organ_number = db.Column(db.Integer)
    fb_or_email_connect = db.Column(db.Boolean)
    income_source = db.Column(db.String(80))
    month_income = db.Column(db.Integer)
    is_before_loan = db.Column(db.Boolean)
    is_activate_loan = db.Column(db.Boolean)
    total_activate_loan = db.Column(db.Integer)
    internet_account_code = db.Column(db.Integer)
    download_loan_db_perm = db.Column(db.Boolean)
    location_perm = db.Column(db.Boolean)
    download_data_phone_perm = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'public_id': self.public_id,
            'full_name': self.full_name,
            'password': self.password,
            'admin': self.admin,
            'post_count': self.posts.count(),
            'post_count': self.posts.count(),
            'post_count': self.posts.count(),
            'post_count': self.posts.count(),
            'post_count': self.posts.count(),
            'post_count': self.posts.count(),
            'post_count': self.posts.count(),
            'post_count': self.posts.count(),
            'post_count': self.posts.count(),
            'post_count': self.posts.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def __repr__(self):
        return '<User {}>'.format(self.full_name)


class Loan_request(db.Model):

    __tablename__ = 'loan_requests'
    id = db.Column(db.Integer, primary_key=True)
   # recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    approved = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    loan_type_id = db.Column(db.Integer, db.ForeignKey('loan_types.id'))
    amount = db.Column(db.Integer)
    days = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    cancel = db.Column(db.Integer, default=0)
    close = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='loan_request',
                                    lazy='dynamic')
    def __repr__(self):
        return '<Loan_request {}>'.format(self.amount)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
   
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    loan_request_id = db.Column(db.Integer, db.ForeignKey('loan_requests.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    text = db.Column(db.Text)
    
    def __repr__(self):
        return '<Comment {}>'.format(self.text)

class Close(db.Model):
    __tablename__ = 'closes'
    id = db.Column(db.Integer, primary_key=True)   
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    loan_request_id = db.Column(db.Integer, db.ForeignKey('loan_requests.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    text = db.Column(db.String(120))
    
    def __repr__(self):
        return '<Comment {}>'.format(self.text)

class Loan_type(db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'loan_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, unique=True)
    amount_from = db.Column(db.Integer, index=True)
    amount_to = db.Column(db.Integer, index=True)
    days_from = db.Column(db.Integer, index=True)
    days_to = db.Column(db.Integer) 
    date_from = db.Column(db.DateTime)
    date_to = db.Column(db.DateTime)
    interest_rate = db.Column(db.Integer)
    interest_type = db.Column(db.String(60), index=True)
    loan_requests = db.relationship('Loan_request', backref='loan_type',
                                lazy='dynamic')
    def __repr__(self):
            return '<Loan_type {}>'.format(self.name)

class Loan_capacity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    account_limit = db.Column(db.Integer, index=True)
    date_from = db.Column(db.DateTime, index=True)
    date_to = db.Column(db.DateTime, index=True)

    def __repr__(self):
            return '<Loan_capacity {}>'.format(self.account_limit)

class Loan_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_request_id = db.Column(db.Integer, db.ForeignKey('loan_requests.id'), index=True)
    start_date = db.Column(db.DateTime, index=True)
    due_date = db.Column(db.DateTime, index=True)
    note = db.Column(db.String(60), index=True)

