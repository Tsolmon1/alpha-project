from flask import abort, render_template, flash, redirect, url_for, g, jsonify, current_app, request
from flask_login import current_user, login_required

from . import home
from ..models import  User, Loan_request, Employee, Notification, Loan_type, Comment, Close
from .forms import  UserAssignForm, RoleForm, RegistrationForm, EditForm, SearchForm, LoanRequestForm, LoanTypeForm, EditLoanTypeForm, CommentForm, CloseForm
from .. import db

from datetime import datetime
from flask_babel import _, get_locale

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter, get_page_args
import logging



@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
   
    """
    List all users
    """
   # check_admin() 
    
    return render_template('home/dashboard.html', title="Dashboard")

@home.route('/register', methods=['GET', 'POST'])
def register():
    form = LoanTypeForm()
    if form.validate_on_submit():
        loan_type = Loan_type(name=form.name.data,
                            amount_from=form.amount_from.data,
                            amount_to=form.amount_to.data,
                            days_from=form.days_from.data,
                            days_to=form.days_to.data,
                            date_from=form.date_from.data,
                            date_to=form.date_to.data,
                            interest_rate=form.interest_rate.data,
                            interest_type=form.interest_type.data)

        # add employee to the database
        db.session.add(loan_type)
        db.session.commit()
        flash('You have successfully registered!')

        # redirect to the login page
        return redirect(url_for('home.loan_type'))

    # load registration template
    return render_template('home/loan_type/loan_type_add.html', form=form, title='LoanTypeAdd')

@home.route('/loan_request')
@login_required
def loan_request():
   
    """
    List all loan_Requests
    """
   # check_admin()
    
    #loan_requests = Loan_request.query.all()
    page = request.args.get('page', 1, type=int)
    loan_requests = Loan_request.query.order_by(Loan_request.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    
    next_url = url_for('home.loan_request', page=loan_requests.next_num) \
        if loan_requests.has_next else None
    prev_url = url_for('home.loan_request', page=loan_requests.prev_num) \
        if loan_requests.has_prev else None

    return render_template('home/loan_request/loan_requests.html', loan_requests=loan_requests.items, title="Loan Requests", next_url=next_url, prev_url=prev_url)

@home.route('/loan_request/<loan_request_id>', methods=['GET'])
@login_required
def get_one_loan_request(current_user, loan_request_id):
    
    loan_request = Loan_request.query.filter_by(id=loan_request_id, user_id=current_user.id).first()

    if not loan_request:
        return jsonify({'message' : 'No loan_request found!'})
    loan_request_data = {}
    loan_request_data['id'] = loan_request.id
    loan_request_data['amount'] = loan_request.amount
    loan_request_data['days'] = loan_request.days
    loan_request_data['approved'] = loan_request.approved
    loan_request_data['loan_type_id'] = loan_request.loan_type_id
    loan_request_data['cancel'] = loan_request.cancel
    loan_request_data['close'] = loan_request.close

    return render_template('home/loan_request/one_loan_request.html', loan_request=loan_request_data, title="Loan Request")

@home.route('/loan_type')
@login_required
def loan_type():
   
    """
    List all loan_Requests
    """
   # check_admin()
    
    loan_types = Loan_type.query.all()

    return render_template('home/loan_type/loan_types.html', loan_types=loan_types, title="Loan Types")



@home.route('/user')
@login_required
def user():
    #users = User.query.all()
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.timestamp.desc()).paginate(
         page, current_app.config['POSTS_PER_PAGE'], False)
    
    next_url = url_for('home.user', page=users.next_num) \
         if users.has_next else None
    prev_url = url_for('home.user', page=users.prev_num) \
         if users.has_prev else None
    #page, per_page, offset = get_page_args(page_parameter='page',
     #                                       per_page_parameter='per_page')
    # search = False
    # q = request.args.get('q')
    # if q:
    #     search = True

    # page = request.args.get(get_page_parameter(), type=int, default=1)

    # users = User.query.all()
   
    # total = len(users)
   
    # pagination = Pagination(page=page, total=total, search=search, record_name='users', css_framework='bootstrap3')

    return render_template('home/user/users.html', users=users.items,  title="User", next_url=next_url, prev_url=prev_url)

  

@home.route('/users/confirm/<int:id>', methods=['GET', 'POST'])
@login_required
def confirm_user(id):
    """
    Assign a department and a role to an employee
    """
#    check_admin()

   # user = User.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    # if not user:
    #     abort(403)

    #form = UserAssignForm(obj=user)
   # request = UserAssignForm(obj=user)
    loan_request = Loan_request.query.filter_by(id=id).first()
   # user = User.query.filter_by(public_id=public_id).first()
    if loan_request.approved == True:
         
        #return jsonify({'message' : 'No user found!'})
         flash('You have successfully unconfirmed a user!', 'success')
         loan_request.approved = False
         
         
    else: 
        flash('You have successfully confirmed a user.', 'success')
        
        loan_request.approved = True
        
    
       
    db.session.commit()
    # if request.approved == True:
    #     flash('Request already confirmed!', 'success')
    # else:
    #     request.approved = True

   # if form.validate_on_submit():       
    
        # db.session.add(request)
        # db.session.commit()
        # flash('You have successfully confirmed a user.')

        # redirect to the roles page
    return redirect(url_for('home.loan_request'))

    return render_template('home/loan_request.html',                      
                           title='Confirm User')

@home.route('/user/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

@home.route('/user/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    Delete a employee from the database
    """
  #  check_admin()

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')

    # redirect to the roles page
    return redirect(url_for('home.user'))
    

@home.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """
    Edit a user
    """
 #   check_admin()

    add_user = False

    user = User.query.get_or_404(id)
    form = EditForm(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.full_name = form.full_name.data
        user.register_number = form.register_number.data
        user.phone_number = form.phone_number.data
        user.civil_number = form.civil_number.data  
        user.email = form.email.data 
        user.address = form.address.data 
        user.relate_phone = form.relate_phone.data 
        user.married = form.married.data 
        user.withlive = form.withlive.data 
        user.home_income = form.home_income.data 
        user.home_member_income = form.home_member_income.data 
        user.educational_level = form.educational_level.data 
        user.is_job = form.is_job.data 
        user.company_name = form.company_name.data 
        user.social_insurance = form.social_insurance.data 
        user.this_company_worked_year = form.this_company_worked_year.data 
        user.worked_organ_number = form.worked_organ_number.data 
        user.income_source = form.income_source.data 
        user.month_income = form.month_income.data 
        user.worked_organ_number = form.worked_organ_number.data 
        user.month_income = form.month_income.data 
        user.is_before_loan = form.is_before_loan.data 
        user.is_activate_loan = form.is_activate_loan.data 
        user.total_activate_loan = form.total_activate_loan.data 
        user.internet_account_code = form.internet_account_code.data 

        db.session.add(user)
        db.session.commit()
        flash('You have successfully edited the employee.')

        # redirect to the roles page
        return redirect(url_for('home.user'))
   
    
    form.email.data = user.email 
    form.full_name.data = user.full_name
    form.register_number.data = user.register_number
    form.phone_number.data = user.phone_number
    form.civil_number.data = user.civil_number
    form.email.data = user.email
    form.address.data = user.address
    form.relate_phone.data = user.relate_phone
    form.married.data = user.married
    form.withlive.data = user.withlive
    form.home_income.data = user.home_income
    form.home_member_income.data = user.home_member_income
    form.educational_level.data = user.educational_level
    form.is_job.data = user.is_job
    form.company_name.data = user.company_name
    form.social_insurance.data = user.social_insurance
    form.this_company_worked_year.data = user.this_company_worked_year
    form.worked_organ_number.data = user.worked_organ_number
    form.month_income.data = user.month_income
    form.is_before_loan.data = user.is_before_loan
    form.is_activate_loan.data = user.is_activate_loan
    form.total_activate_loan.data = user.total_activate_loan
    form.internet_account_code.data = user.internet_account_code

    return render_template('home/user/user_edit.html', add_user=add_user,
                           form=form, title="Edit User")

@home.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    #g.locale = str(get_locale())

@home.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('home.loan_request'))
    page = request.args.get('page', 1, type=int)
    users, total = User.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('home.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('home.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    
    if not g.search_form.validate():
        return redirect(url_for('home.user'))
    page = request.args.get('page', 1, type=int)
    users, total = User.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('home.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('home.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None

    return render_template('home/search.html', title=('Search'), users=users,
                           next_url=next_url, prev_url=prev_url)



@home.route('/employee/<username>')
@login_required
def employee(username):
    employee = Employee.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    loan_requests = employee.loan_requests.order_by(Loan_request.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('home.dashoard', username=employee.username,
                       page=loan_requests.next_num) if loan_requests.has_next else None
    prev_url = url_for('home.dashoard', username=employee.username,
                       page=loan_requests.prev_num) if loan_requests.has_prev else None
    return render_template('admin/employees/employee.html', employee=employee, loan_requests=loan_requests.items,
                           next_url=next_url, prev_url=prev_url)

@home.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

@home.route('/loan_type/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_loan_type(id):
    """
    Edit a loan type
    """


    add_loan_type = False

    loan_type = Loan_type.query.get_or_404(id)
    form = EditLoanTypeForm(obj=loan_type)
    if form.validate_on_submit():
        loan_type.name = form.name.data
        loan_type.amount_from = form.amount_from.data
        loan_type.amount_to = form.amount_to.data
        loan_type.days_from = form.days_from.data
        loan_type.days_to = form.days_to.data
        loan_type.date_from = form.date_from.data
        loan_type.date_to = form.date_to.data
        loan_type.interest_rate = form.interest_rate.data
        loan_type.interest_type = form.interest_type.data

        db.session.add(loan_type)
        db.session.commit()
        flash('You have successfully edited the loan_type.')

        # redirect to the roles page
        return redirect(url_for('home.loan_type'))

    form.name.data = loan_type.name
    form.amount_from.data = loan_type.amount_from
    form.amount_to.data = loan_type.amount_to
    form.days_from.data = loan_type.days_from
    form.days_to.data = loan_type.days_to
    form.date_from.data = loan_type.date_from
    form.date_to.data = loan_type.date_to
    form.interest_rate.data = loan_type.interest_rate
    form.interest_type.data = loan_type.interest_type

    return render_template('home/loan_type/loan_type_edit.html', add_loan_type=add_loan_type,
                           form=form, title="Edit Loan Type")

@home.route('/loan_type/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_loan_type(id):
    """
    Delete a loan_type from the database
    """ 

    loan_type = Loan_type.query.get_or_404(id)
    db.session.delete(loan_type)
    db.session.commit()
    flash('You have successfully deleted the loan_type.')

    # redirect to the roles page
    return redirect(url_for('home.loan_type'))

@home.route('/comment/<int:id>', methods=['GET', 'POST'])
def comment(id):
    employees = Employee.query.all()
    
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, employee_id=current_user.id, loan_request_id=id)

        # add employee to the database
        db.session.add(comment)
        db.session.commit()
        #flash('You have successfully canceled!')

        # redirect to the login page
        
        
        
        loan_request = Loan_request.query.filter_by(id=id).first()
            # user = User.query.filter_by(public_id=public_id).first()
        if loan_request.cancel == True:
         
            #return jsonify({'message' : 'No user found!'})
                   
            flash('You have unsuccessfully canceled a user.', 'success')
        
            loan_request.cancel = False
         
        else: 
            loan_request.cancel = True 
            flash('You have successfully canceled a user!', 'success')
             
        db.session.commit()
        return redirect(url_for('home.loan_request'))
        
    # load registration template
    return render_template('home/loan_request/comment.html', form=form, title='Comment', employees=employees)

@home.route('/finished/<int:id>', methods=['GET', 'POST'])
def finished(id):
    employees = Employee.query.all()
    
    form = CloseForm()
    if form.validate_on_submit():
        close = Close(text=form.text.data, employee_id=current_user.id, loan_request_id=id)

        # add employee to the database
        db.session.add(close)
        db.session.commit()
        #flash('You have successfully canceled!')

        # redirect to the login page
        
        
        
        loan_request = Loan_request.query.filter_by(id=id).first()
            # user = User.query.filter_by(public_id=public_id).first()
        if loan_request.close == True:
         
            #return jsonify({'message' : 'No user found!'})
                   
            flash('You have unsuccessfully closed a user.', 'success')
        
            loan_request.close = False
         
        else: 
            loan_request.close = True 
            flash('You have successfully closed a user!', 'success')
             
        db.session.commit()
        return redirect(url_for('home.loan_request'))
        
    # load registration template
    return render_template('home/loan_request/comment.html', form=form, title='Comment', employees=employees, loan_request_id=id)

@home.route('/user/<user_id>', methods=['GET'])
@login_required
def get_one_user(user_id):
    
    users = User.query.filter_by(id=user_id).first()

    if not users:
        return jsonify({'message' : 'No user found!'})
    user_data = {}
    user_data['id'] = users.id
    user_data['email'] = users.email 
    user_data['full_name'] = users.full_name
    user_data['register_number'] = users.register_number
    user_data['phone_number'] = users.phone_number
    user_data['civil_number'] = users.civil_number
    user_data['email'] = users.email
    user_data['address'] = users.address
    user_data['relate_phone'] = users.relate_phone
    user_data['married'] = users.married
    user_data['withlive'] = users.withlive
    user_data['home_income'] = users.home_income
    user_data['home_member_income'] = users.home_member_income
    user_data['educational_level'] = users.educational_level
    user_data['is_job'] = users.is_job
    user_data['company_name'] = users.company_name
    user_data['social_insurance'] = users.social_insurance
    user_data['this_company_worked_year'] = users.this_company_worked_year
    user_data['worked_organ_number'] = users.worked_organ_number
    user_data['month_income'] = users.month_income
    user_data['is_before_loan'] = users.is_before_loan
    user_data['is_activate_loan'] = users.is_activate_loan
    user_data['total_activate_loan'] = users.total_activate_loan
    user_data['internet_account_code'] = users.internet_account_code

    return render_template('home/user/one_user.html', users=user_data, title="User")

@home.route('/loan_type/<loan_type_id>', methods=['GET'])
@login_required
def get_one_loan_type(loan_type_id):
    
    loan_type = Loan_type.query.filter_by(id=loan_type_id).first()

    if not loan_type:
        return jsonify({'message' : 'No loan_type found!'})
    loan_type_data = {}
    loan_type_data['id'] = loan_type.id
    loan_type_data['name'] = loan_type.name
    loan_type_data['amount_from'] = loan_type.amount_from
    loan_type_data['amount_to'] = loan_type.amount_to
    loan_type_data['days_from'] = loan_type.days_from
    loan_type_data['days_to'] = loan_type.days_to
    loan_type_data['date_from'] = loan_type.date_from
    loan_type_data['date_to'] = loan_type.date_to
    loan_type_data['interest_rate'] = loan_type.interest_rate
    loan_type_data['interest_type'] = loan_type.interest_type

    return render_template('home/loan_type/one_loan_type.html', loan_type=loan_type_data, title="Loan Type")