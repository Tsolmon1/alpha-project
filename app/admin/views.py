from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import  EmployeeAssignForm, RoleForm, RegistrationForm, EditForm
#from ..auth.forms import  RegistrationForm
from .. import db
from ..models import  Employee, Role


def check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)


# Department Views


#@admin.route('/departments', methods=['GET', 'POST'])

@admin.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('admin.list_employees'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

# Role Views


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

   # return render_template(title="Delete Role")

@admin.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    """
    Edit a employee
    """
    check_admin()

    add_employee = False

    employee = Employee.query.get_or_404(id)
    form = EditForm(obj=employee)
    if form.validate_on_submit():
        employee.email = form.email.data
        employee.username = form.username.data
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
             
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully edited the employee.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    form.email.data = employee.email
    form.username.data = employee.username
    form.first_name.data = employee.first_name
    form.last_name.data = employee.last_name
   
    return render_template('admin/employees/employee_edit.html', add_employee=add_employee,
                           form=form, title="Edit Employee")


@admin.route('/employee/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Delete a employee from the database
    """
    check_admin()

    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted the operator.')

    # redirect to the roles page
    return redirect(url_for('admin.list_employees'))

  #  return render_template(title="Delete Employee")


# Employee Views

@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')
