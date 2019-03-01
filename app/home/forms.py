from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, BooleanField, IntegerField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from ..models import  Role, Employee, User, Loan_request, Comment
from flask import request
from flask_babel import lazy_gettext as _l

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')

class CommentForm(FlaskForm):
    """
    Form for users to create new account
    """

    text = StringField('Text', validators=[DataRequired()])
    

    submit = SubmitField('Submit')


class CloseForm(FlaskForm):
    """
    Form for users to create new account
    """

    text = StringField('Text', validators=[DataRequired()])
    

    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    """
    Form for users to create new account
    """
   
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full_name', validators=[DataRequired()])
    register_number = StringField('Register_number', validators=[DataRequired()])
    phone_number = StringField('Phone_number', validators=[DataRequired()])  
    civil_number = StringField('Civil_number', validators=[DataRequired()])  
    address = StringField('Address', validators=[DataRequired()])
    relate_phone = StringField('Relate_phone', validators=[DataRequired()]) 
  
    married = BooleanField('married', validators=[DataRequired()], default=False)
    home_income = StringField('Home_income', validators=[DataRequired()])
    home_member_income = StringField('Home_member_income', validators=[DataRequired()])
    withlive = StringField('Withlive', validators=[DataRequired()])  
    educational_level = StringField('Educational_level', validators=[DataRequired()])    
    is_job = BooleanField('is_job', validators=[DataRequired()])
    company_name = StringField('Company_name', validators=[DataRequired()])
    this_company_worked_year = StringField('This_company_worked_year', validators=[DataRequired()])
    worked_organ_number = StringField('Worked_organ_number', validators=[DataRequired()]) 
    income_source = StringField('Income_source', validators=[DataRequired()])
    month_income = StringField('Month_income', validators=[DataRequired()])    
    is_activate_loan = BooleanField('is_activate_loan', validators=[DataRequired()])
    total_activate_loan = StringField('Total_activate_loan', validators=[DataRequired()])    
    is_before_loan = BooleanField('is_before_loan', validators=[DataRequired()])
    internet_account_code = StringField('Internet_account_code', validators=[DataRequired()])
    social_insurance = BooleanField('social_insurance', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoanRequestForm(FlaskForm):
    """
    Form for users to create new account
    """
   
  
    approved = StringField('Approved', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    days = IntegerField('Days', validators=[DataRequired()])
    loan_type_id = IntegerField('Days', validators=[DataRequired()])
    
    cancel = IntegerField('Cancel', validators=[DataRequired()])
    submit = SubmitField('Submit')
class LoanTypeForm(FlaskForm):
    """
    Form for users to create new account
    """   
  
    name = StringField('Name', validators=[DataRequired()])
    amount_from = IntegerField('Amount_from', validators=[DataRequired()])
    amount_to = IntegerField('Amount_to', validators=[DataRequired()])
    days_from = IntegerField('Days_from', validators=[DataRequired()])
    days_to = IntegerField('Days_to', validators=[DataRequired()])
    date_from = DateField('Date_from', format='%Y-%m-%d')
    date_to = DateField('Date_to', format='%Y-%m-%d')
    interest_rate = StringField('Interest_rate', validators=[DataRequired()])
    #interest_type = StringField('Interest_type', validators=[DataRequired()])
    interest_type = SelectField('Interest_type',choices=[('month','month'), ('day','day')])
    submit = SubmitField('Submit')



class EditLoanTypeForm(FlaskForm):
    """
    Form for users to create new account
    """
    name = StringField('Name', validators=[DataRequired()])
    amount_from = IntegerField('Amount_from', validators=[DataRequired()])
    amount_to = IntegerField('Amount_to', validators=[DataRequired()])
    days_from = IntegerField('Days_from', validators=[DataRequired()])
    days_to = IntegerField('Days_to', validators=[DataRequired()])
    date_from = DateField('Date_from', format='%Y-%m-%d')
    date_to = DateField('Date_to', format='%Y-%m-%d')
    interest_rate = StringField('Interest_rate', validators=[DataRequired()])
    interest_type = SelectField('Interest_type',choices=[('month','month'), ('day','day')])
    submit = SubmitField('Submit')

class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))  

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """

class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


   
