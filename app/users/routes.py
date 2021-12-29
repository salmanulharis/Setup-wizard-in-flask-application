import os
import random
import string
import stripe
import json
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Address, Job, Product
from app.users.forms import RegistrationForm, LoginForm, ProfileForm, AddressForm, JobDetailsForm, ProductForm
from app.users.utils import save_picture
# from app.subscriptions.utils import create_subscription
from app.tenantity import Tenantity

from opentok import MediaModes


users = Blueprint('users', __name__)

@users.route('/register', methods=['POST', 'GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('users.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, image_file='default.png', new_user=True)
		# Tenantity.create(form.username.data)
		# Tenantity.switch('public')
		db.session.add(user)
		db.session.commit()

		flash(f'Your account has been created!', 'success')          #flash is a bootstrap thing imported through flask
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('users.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')

			# if not Subscription.query.filter_by(user_id=current_user.id).first():
			# 	create_subscription(0, 'active')

			return redirect(next_page) if next_page else redirect(url_for('users.home'))
		else:
			flash('Login Unsuccesfull! please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('users.login'))



@users.route('/home')
@users.route('/')
@login_required
def home():
	# subs_history = Subscription.query.filter_by(user_id=current_user.id, status='active').first()
	# if not subs_history:
	# 	return redirect(url_for('subscriptions.sub_approve'))
	addressform = AddressForm()
	jobform = JobDetailsForm()
	productform = ProductForm()
	address_exist = Address.query.filter_by(user_id=current_user.id).first()
	job_exist = Job.query.filter_by(user_id=current_user.id).first()
	product_exist = Product.query.filter_by(user_id=current_user.id).first()
	if address_exist and job_exist and product_exist:
		new_user = 0
	else:
		new_user = 1

	print(new_user)
	if address_exist:
		addressform.fullname.data = address_exist.fullname
		addressform.phone.data = address_exist.phone
		addressform.city.data = address_exist.city

	if job_exist:
		jobform.jobname.data = job_exist.jobname
		jobform.experience.data = job_exist.experience
		jobform.company.data = job_exist.company

	if product_exist:
		productform.product.data = product_exist.product
		productform.price.data = product_exist.price
		productform.validity.data = product_exist.validity
		productform.description.data = product_exist.description

	user = current_user.username
	return render_template('home.html', user=current_user.username, subs_history='subs_history', new_user=new_user,
	 addressform=addressform, jobform=jobform, productform=productform)

@login_required
@users.route('/user_details', methods=['POST', 'GET'])
def user_details():
	user = current_user
	form = ProfileForm()
	return render_template('details.html', user=user.username, form=form)

@login_required
@users.route('/save_address', methods=['POST', 'GET'])
def save_address():
	address = Address()
	address_exist = Address.query.filter_by(user_id=current_user.id).first()
	if address_exist:
		address_exist.fullname = request.args['fullname']
		address_exist.phone = request.args['phone']
		address_exist.city = request.args['city']
	else:
		address.fullname = request.args['fullname']
		address.phone = request.args['phone']
		address.city = request.args['city']
		address.user_id = current_user.id
		db.session.add(address)
	db.session.commit()
	return "success"

@login_required
@users.route('/save_job', methods=['POST', 'GET'])
def save_job():
	job = Job()
	job_exist = Job.query.filter_by(user_id=current_user.id).first()
	if job_exist:
		job_exist.jobname = request.args['jobname']
		job_exist.experience = request.args['experience']
		job_exist.company = request.args['company']
	else:
		job.jobname = request.args['jobname']
		job.experience = request.args['experience']
		job.company = request.args['company']
		job.user_id = current_user.id
		db.session.add(job)
	db.session.commit()
	return "success"

@login_required
@users.route('/save_product', methods=['POST', 'GET'])
def save_product():
	print(request.args)
	products = Product()
	product_exist = Product.query.filter_by(user_id=current_user.id).first()
	if product_exist:
		product_exist.product = request.args['product']
		product_exist.price = request.args['price']
		product_exist.validity = request.args['validity']
		product_exist.description = request.args['description']
	else:
		products.product = request.args['product']
		products.price = request.args['price']
		products.validity = request.args['validity']
		products.description = request.args['description']
		products.user_id = current_user.id
		db.session.add(products)
	db.session.commit()
	return "success"






# @users.route('/add_address', methods=['GET','POST'])
# def add_address():
#     form = AddressForm()
#     url = request.referrer
#     return render_template('address.html', form=form, url=url, heading='Add Address', submit='Save Address')

# @users.route('/edit_address', methods=['GET','POST'])
# def edit_address():
#     form = AddressForm()
#     current_address = Shipping.query.filter_by(user_id=current_user.id).first()
#     add = json.loads(current_address.address)

#     form.fullname.data = add['fullname']
#     form.phone.data = add['phone']
#     form.pin_code.data = add['pin_code']
#     form.state.data = add['state']
#     form.city.data = add['city']
#     form.building.data = add['building']

#     url = request.referrer
#     return render_template('address.html', form=form, url=url, heading='Edit Address', submit='Edit Address')

# @users.route('/save_address', methods=['POST', 'GET'])
# def save_address():
# 	shipping = Shipping()
# 	has_address = Shipping.query.filter_by(user_id=current_user.id).first()
	
# 	address_form = request.form
# 	address = dict(address_form)
# 	url = address['url']
# 	del address['csrf_token']
# 	del address['submit']
# 	del address['url']

# 	if has_address:
# 		has_address.user_id = current_user.id
# 		has_address.address = json.dumps(address)
# 	else:
# 		shipping.user_id = current_user.id
# 		shipping.address = json.dumps(address)
# 		db.session.add(shipping)
# 	db.session.commit()

# 	return redirect(url)


