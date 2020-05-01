from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User, Company, CompanyData


class LoginForm(FlaskForm):
    user_id = StringField('UserID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    user_id = StringField('UserID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_user_id(self, user_id):
        user = User.query.filter_by(user_id=user_id.data).first()
        if user is not None:
            raise ValidationError('UserID already exists. Try with a different one.')

    
class CompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    address1 = StringField('Address1', validators=[DataRequired()])
    address2 = StringField('Address2', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postal_code = IntegerField('Postal Code', validators=[DataRequired()]) 
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Add Company')

    def validate_company_name(self, name):
        company = Company.query.filter_by(name=name.data).first()
        if company is not None:
            raise ValidationError('Company already exists. Duplication not allowed')

class CompanyDataForm(FlaskForm):
    company_name = QuerySelectField('Company Name', query_factory=Company.query.order_by(Company.name).all(), validators=[DataRequired()])
    #RadioField('Company Name', choices=tuple(Company.query.order_by(Company.name).all()), validators=[DataRequired()], validate_choice=True)
    financial_year = IntegerField('Financial Year', validators=[DataRequired()])
    annual_sales = IntegerField('Annual Sales', validators=[DataRequired()])
    book_value_equity = IntegerField('Book Value of Equity', validators=[DataRequired()])
    total_current_assets = IntegerField('Total Current Assets', validators=[DataRequired()])
    total_current_liabilities = IntegerField('Total Current Liabilites', validators=[DataRequired()])
    earnings_before_interest_tax = IntegerField('Earnings Before Interest & Taxes', validators=[DataRequired()]) 
    retained_earnings = IntegerField('Retained Earnings', validators=[DataRequired()])
    # To be calculated, at the same time, the option of manual entering is also allowed
    BRS = IntegerField('BRS')
    BRZ = StringField('BRZ')
    submit = SubmitField('Submit Data')
    
    def validate_financial_year(self,financial_year):
        company_data = CompanyData.query.filter_by(financial_year=financial_year.data).first()
        if company_data is not None:
            raise ValidationError('The company {} already has data for this year'.format(company_name.data))
    
    def validate_name(self,name):
        company_data = Company.query.filter_by(name=company_name.data).first()
        if company_data is None:
            raise ValidationError('There is no such company in the database. Enter Company details first.')

class CompanyQueryForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    #RadioField('Choose the name of the Company', choices=tuple(Company.query.order_by(Company.name).all()), validators=[DataRequired()])
#year = RadioField('Choose the Financial Year', choices=CompanyData.query.filter_by(company_name=name.data).all(), validators=[DataRequired()])
    submit = SubmitField('Show')
    
    def validate_name(self,name):
        company_data = Company.query.filter_by(name=name.data).first()
        if company_data is None:
            raise ValidationError('There is no such company in the database. Enter Company details first.')

class EditCompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    address1 = StringField('Address1', validators=[DataRequired()])
    address2 = StringField('Address2', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postal_code = IntegerField('Postal Code', validators=[DataRequired()]) 
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Add Company')

class CompanyUpload(FlaskForm):
    file = FileField('Export Company (excel)', validators=[FileRequired(), FileAllowed (['xls','xlsx','csv'], "Spreadsheet Only!")])
    submit = SubmitField('Upload')

class CompanyDataUpload(FlaskForm):
    file = FileField('Export Company Data (Excel)', validators=[FileRequired(), FileAllowed (['xls','xlsx','csv'], "Spreadsheet Only!")])
    submit = SubmitField('Upload')