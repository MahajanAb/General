from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    user_number = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    designation = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.user_id)   

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)        
        
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    address1 = db.Column(db.String(128), index=True)
    address2 = db.Column(db.String(128), index=True)
    street = db.Column(db.String(128), index=True)
    city = db.Column(db.String(64), index=True)
    postal_code = db.Column(db.String(64), index=True)
    country = db.Column(db.String(64), index=True)
    company_data = db.relationship('CompanyData', back_populates='company')

def __repr__(self):
    return '<Company {}>'.format(self.name)

class CompanyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    financial_year = db.Column(db.Integer, index=True, unique=True)
    annual_sales = db.Column(db.Integer, index=True)
    book_value_equity = db.Column(db.Integer, index=True)
    total_current_assets = db.Column(db.Integer, index=True)
    total_current_liabilities = db.Column(db.Integer, index=True)
    earnings_before_interest_tax = db.Column(db.Integer, index=True)
    retained_earnings = db.Column(db.Integer, index=True)
    BRS = db.Column(db.Integer, index=True)
    BRZ = db.Column(db.String(64), index=True)
    company_name = db.Column(db.String(128), db.ForeignKey('company.name'))
    company = db.relationship("Company", back_populates='company_data')

def __repr__(self):
    return '<Year {} CompanyName {}>'.format(self.financial_year, self.company_name)    
    