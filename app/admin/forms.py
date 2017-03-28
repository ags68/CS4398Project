# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField, BooleanField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, AnyOf
from ..models import Employee, Payroll, Compensation


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    id = StringField('Employee ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=60)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=60)])
    middle_name = StringField('Middle Name', validators=[Length(min=1, max=60)])
    home_address = StringField('Home Address', validators=[DataRequired(), Length(max=60)])
    mailing_address = StringField('Mailing Address', validators=[DataRequired(), Length(max=60)])
    home_phone = StringField('Home Phone', validators=[Length(max=15)])
    cell_phone = StringField('Cell Phone', validators=[DataRequired(), Length(max=15)])

    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_emp_id(self, field):
        if Employee.query.filter_by(id=field.data).first():
            raise ValidationError('Employee ID is already in use.')



class PersonalInfoForm(FlaskForm):
    """
    Form for admin to edit employee personal info
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=60)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=60)])
    middle_name = StringField('Middle Name', validators=[Length(min=1, max=60)])
    home_address = StringField('Home Address', validators=[DataRequired(), Length(max=60)])
    mailing_address = StringField('Mailing Address', validators=[DataRequired(), Length(max=60)])
    home_phone = StringField('Home Phone', validators=[Length(max=15)])
    cell_phone = StringField('Cell Phone', validators=[DataRequired(), Length(max=15)])
    submit = SubmitField('Submit')

class PayrollForm(FlaskForm):
    """
    Form for admin to edit employee personal info
    """
    eid = StringField('Employee ID', validators=[DataRequired(), ])
    account_type = StringField('Account Type', validators=[DataRequired(), AnyOf(['Checking', 'Savings'])])
    account_num = StringField('Account Number', validators=[DataRequired(), Length(min=9, max=9)])
    routing_num = StringField('Routing Number', validators=[DataRequired(), Length(min=9, max=9)])
    amount_withheld = IntegerField('Amount Withheld', validators=[ NumberRange(min=0)])
    num_allowances = IntegerField('Number of Allowances', validators=[ NumberRange(min=0)])
    claim_exemption = StringField('Claim Exemption', validators=[DataRequired(), AnyOf(['True', 'False', 'Yes', 'No'])])
    submit = SubmitField('Submit')
    
    def validate_eid(self, field):
        if Employee.query.filter_by(id=field.data).first() == None:
            raise ValidationError('Employee ID not found.')
        if Payroll.query.filter_by(eid=field.data).first():
            raise ValidationError('Payroll info has already been entered for this employee.')

class CompensationForm(FlaskForm):
    """
    Form for admin to edit employee compensation info
    """
    eid = StringField('Employee ID', validators=[DataRequired()])
    pay_period = StringField('Pay Period', validators=[DataRequired()])
    net_pay = DecimalField('Net Pay', validators=[DataRequired()])
    gross_pay = DecimalField('Gross Pay', validators=[DataRequired()])
    hourly_wage = DecimalField('Hourly Wage', validators=[DataRequired()])
    hours_worked = DecimalField('Hours Worked', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_eid(self, field):
        if Employee.query.filter_by(id=field.data).first() == None:
            raise ValidationError('Employee ID not found.')
