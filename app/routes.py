from flask import render_template, flash, redirect, url_for, request, send_file
from app import app
from app.forms import LoginForm, RegistrationForm, CompanyForm, CompanyDataForm, CompanyQueryForm, EditCompanyForm, CompanyUpload, CompanyDataUpload
from app import db
from app.models import User, Company, CompanyData
from app.calculate import calculator
from werkzeug.utils import secure_filename
import os
import pandas as pd
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', user_id='Candidate, proceed to Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid UserId or password', category='error')
            return redirect(url_for('login', user_id=user))
        return redirect(url_for('company')) #user_id=form.user_id.data))
    return render_template('login.html', title='Sign In', form=form)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_check=User.query.filter_by(user_id=form.user_id.data).first()
        if user_check is None:
            user = User(user_id=form.user_id.data, name=form.name.data, designation=form.designation.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', category='message')
            return redirect(url_for('login'))
        flash('User_ID already taken! Try a different one', 'error')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route('/company', methods = ['GET', 'POST'])
def company():
    form = CompanyForm()
    if form.validate_on_submit():
        company_check = Company.query.filter_by(name=form.name.data).first()
        if company_check is None:
            company = Company(name=form.name.data, address1=form.address2.data, address2=form.address2.data,
                            street=form.street.data, city=form.city.data, postal_code=form.postal_code.data, 
                            country=form.country.data)
            db.session.add(company)
            db.session.commit()
            flash('New company added!', category='message')
            return redirect(url_for('companydata'))
        flash('This name is already in the database!', 'info')
        return redirect(url_for('company'))
    return render_template('company.html', title='Add Company', form=form)

@app.route('/companydata', methods = ['GET', 'POST'])
def companydata():
    form = CompanyDataForm()
    if form.validate_on_submit():
        name_check = Company.query.filter_by(name=form.company_name.data).first()
        year_check = CompanyData.query.filter_by(financial_year=form.financial_year.data).all()
        if name_check is not None and year_check is None:
            company_data = CompanyData(company_name=form.company_name.data, financial_year=form.financial_year.data, 
                annual_sales=form.annual_sales.data, book_value_equity=form.book_value_equity.data,
                total_current_assets=form.total_current_assets.data, total_current_liabilities=form.total_current_assets.data, 
                earnings_before_interest_tax=form.earnings_before_interest_tax.data,
                retained_earnings=form.retained_earnings.data, BRS=calculator(company_data)[0], BRZ=calculator(company_data)[1])
            calculator(company_data)          
            db.session.add(company)
            db.session.commit()

            flash('Data for the year {} of {} company added!'.format(form.financial_year.data, form.company_name.data), category='message')
            return(redirect(url_for('companydata')))
        flash('This company does not exist. Create company profile first', 'warning')
        return redirect(url_for('company'))
    return render_template('companydata.html', title='Add Company Data', form=form)

@app.route('/companyquery', methods = ['GET', 'POST'])
def company_query():
    form = CompanyQueryForm()
    if form.validate_on_submit():
        name_check = Company.query.filter_by(name=form.name.data).first()
        if name_check is not None:
            company_data = CompanyData.query.filter_by(company_name=form.name.data).all()
            ##add name condition too to the years below
            #needed?
            #year_check = CompanyData.query.order_by(CompanyData.financial_year).all()
            flash(company_data)
            flash('success', category='message')
            return redirect(url_for('company_display', name=form.name.data))
        flash('No such company exists', 'warning')
        return redirect(url_for('company_query'))
    flash('Try Again', 'error')
    return render_template('companyquery.html', form=form)

#now go to compnaydisplay
#data = CompanyData.query.filter_by(name=form.name.data).first_or_404()
@app.route('/companydisplay/<name>')
def company_display(name):
    name = request.args.get('name')
    company_data = CompanyData.query.order_by(CompanyData.financial_year).all()
    return render_template('companydisplay.html', company_data=company_data)

@app.route('/editcompany', methods=['GET', 'POST'])
def edit_company():
    form = EditCompanyForm()
    if form.validate_on_submit():
        company = Company.query.filter_by(name=form.name.data).first()
        
        company.address1 = form.address1.data
        company.address2 = form.address2.data
        company.street = form.street.data
        company.city = form.city.data 
        company.postal_code = form.postal_code.data
        company.country = form.country.data 
        
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_company'))
    """elif request.method == 'GET':    Autofilled when company is defined
        #form.name.data = company.name
        form.address1.data = company.address1 
        form.address2.data = company.address2
        form.street.data = company.street
        form.city.data = company.city
        form.postal_code.data = company.postal_code
        form.country.data = company.country"""       
    return render_template('editcompany.html', title='Edit Company', form=form)

@app.route('/uploadcompany', methods=['GET','POST'])
def upload_company():
    form = CompanyUpload()
    if form.validate_on_submit():
        f = form.excel.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.instance_path, 'companyexcel', filename))
        return redirect(url_for('index'))
    return render_template('uploadcompany.html', form=form)

@app.route('/uploadcompanydata', methods=['GET','POST'])
def upload_companydata():
    form = CompanyDataUpload()
    if form.validate_on_submit():
        f = form.excel.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.instance_path, 'companydataexcel', filename))
        return redirect(url_for('index'))
    return render_template('uploadcompanydata.html', form=form)

#Template for reading from saved excel files using pandas
@app.route("/tables")
def show_tables():
    data = pd.read_excel('dummy_data.xlsx')
    data.set_index(['Name'], inplace=True)
    data.index.name=None
    females = data.loc[data.Gender=='f']
    males = data.loc[data.Gender=='m']
    #DataFrame.to_sql(self, name: str, con, schema=None, if_exists: str = 'fail', index: bool = True, index_label=None, chunksize=None, dtype=None, method=None) 
    return render_template('view.html',tables=[females.to_html(classes='female'), males.to_html(classes='male')], titles = ['na', 'Female attrib', 'Male attrib'])

#template for generating and displaying histograms for BRZ value across year. Use filter_by for a single year, 
# and POST method with form to ask user for input 
@app.route("/charts.png")
def charts():
    df = pd.read_sql_query(CompanyData.query.order_by(CompanyData.year).all()) # over here df
    histogram = df.hist(column='BRZ', bins=6)
    canvas = FigureCanvas(histogram)
    img = io.BytesIO()
    charts.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

#for pearson correlation use: DataFrame.corr(self, method='pearson', min_periods=1) on df
#mean - df['column_name'].mean(), median - df.median(), mode - df.mode(), standard deviation - df.std()