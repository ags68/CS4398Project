from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employee'

    

    id = db.Column(db.Integer, primary_key=True)

    #employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    middle_name = db.Column(db.String(60), index=True)
    dob = db.Column(db.Date, index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    street = db.Column(db.String(60), index=True)
    city = db.Column(db.String(60), index=True)
    state = db.Column(db.String(60), index=True)
    zip = db.Column(db.Integer, index=True)
    home_phone = db.Column(db.String(60), index=True)
    cell_phone = db.Column(db.String(60), index=True)
    payroll = db.relationship("Payroll", uselist=False, back_populates="employee")
    compensations = db.relationship("Compensation", back_populates="employee")
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

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

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))



class Payroll(db.Model):
    """
    Create a Payroll table
    """

    __tablename__ = 'payroll_info'

    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(60), index=True)
    account_num = db.Column(db.String(60), index=True)
    routing_num = db.Column(db.String(60), index=True)
    amount_withheld = db.Column(db.Integer, index=True)
    num_allowances = db.Column(db.Integer, index=True)
    claim_exemption = db.Column(db.Boolean, index=True)
    eid = db.Column(db.Integer, db.ForeignKey('employee.id'))
    employee = db.relationship('Employee', back_populates='payroll')

    def __repr__(self):
        return '<Payroll: {}>'.format(self.name)

class Compensation(db.Model):
    """
    Create a Compensation table
    """

    __tablename__ = 'compensation_info'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, index=True)
    end_date = db.Column(db.Date, index=True)
    net_pay = db.Column(db.Float, index=True)
    gross_pay = db.Column(db.Float, index=True)
    hourly_wage = db.Column(db.Float, index=True)
    hours_worked = db.Column(db.Float, index=True)
    eid = db.Column(db.Integer, db.ForeignKey('employee.id'))
    employee = db.relationship("Employee", back_populates="compensations")

    def __repr__(self):
        return '<Compensation: {}>'.format(self.name)
