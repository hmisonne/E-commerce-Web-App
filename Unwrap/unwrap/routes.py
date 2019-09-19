import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from unwrap import app, db, bcrypt
from unwrap.forms import RegistrationForm, LoginForm, UpdateAccountForm
from unwrap.models import User, Products, Cart
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func, update

def getLoginDetails():
    if current_user.is_authenticated:
        noOfItems = Cart.query.filter_by(buyer=current_user).count()
    else:
        noOfItems = 0
    return noOfItems

@app.route("/")
@app.route("/home")
def home():
    noOfItems = getLoginDetails()
    return render_template('home.html', noOfItems=noOfItems)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(lastname=form.lastname.data,firstname=form.firstname.data,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.lastname = form.lastname.data
        current_user.firstname = form.firstname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.lastname.data = current_user.lastname
        form.firstname.data = current_user.firstname
        form.email.data = current_user.email
    return render_template('account.html', title='Account',
                           form=form)

# @app.route("/partners")
# def partners():
#      return render_template("partners.html", title='Partners')

# @app.route("/products-list")
# def products_list():
#      return render_template("products-list.html", title='Products list')

@app.route("/unwrap-project")
def unwrap_project():
    noOfItems = getLoginDetails()
    return render_template("unwrap-project.html", title='The project', noOfItems=noOfItems)


@app.route("/how-it-works")
def how_it_works():
     return render_template("how-it-works.html", title='How it works')


@app.route("/select_products", methods=['GET', 'POST'])
def select_products():
    noOfItems = getLoginDetails()
    products = Products.query.all()
    return render_template('select_products.html', products=products,noOfItems=noOfItems)



@app.route("/addToCart/<int:product_id>")
@login_required
def addToCart(product_id):
    product = Products.query.get_or_404(product_id)
    item_to_add = Cart(product_id=product.id, buyer=current_user)
    db.session.add(item_to_add)
    db.session.commit()
    flash('Your item has been added to your cart!', 'success')
    return redirect(url_for('select_products'))


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    noOfItems = getLoginDetails()
    cart = Products.query.join(Cart).filter_by(buyer=current_user).all()
    subtotal = 0
    for item in cart:
        subtotal+=int(item.price)

    # if request.method == "POST":
    #     qty = request.form.get("qty")
    #     idpd = request.form.get("idpd")
    #     stmt = update(Cart).where(product_id==idpd).values(quantity=qty)
    return render_template('cart.html', cart=cart, noOfItems=noOfItems, subtotal=subtotal)

@app.route("/removeFromCart/<int:product_id>")
@login_required
def removeFromCart(product_id):

    item_to_remove = Cart.query.filter_by(product_id=product_id, buyer=current_user).first()
    db.session.delete(item_to_remove)
    db.session.commit()
    flash('Your item has been removed from your cart!', 'success')
    return redirect(url_for('cart'))