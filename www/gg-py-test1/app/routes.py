from flask import render_template, flash, redirect, url_for, request
from app import app, db
from config import Config
from app.forms import LoginForm, CreateAccountForm, RegistrationForm, SearchForm
from app.models import Account, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy import or_


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('accounts'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('accounts')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('accounts'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    return render_template('user.html', user=user)


account_prev_page = 1


@app.route('/accounts', methods=['GET', 'POST'])
@app.route('/accounts/<int:page>', methods=['GET', 'POST'])
@login_required
def accounts(page=1):
    global account_prev_page
    account_prev_page = page
    form = SearchForm()
    if request.args.get('search_value', None) != None:
        query = request.args.get('search_value')
    else:
        query = form.data['search']
    if query != None:
        p = Account.query.filter(or_(Account.nickname.ilike('%'+query+'%'), Account.clanname.ilike('%'+query+'%'))).paginate(page, Config.PAGE_ROWS_COUNT, False)
        accounts = p.items
        pagpages = {'has_prev': p.has_prev, 'has_next': p.has_next, 'prev_num': p.prev_num, 'next_num': p.next_num}
        return render_template('accounts.html', form=form, query=query, accounts=accounts, pagpages=pagpages, search_value=query)
    p = Account.query.paginate(page, Config.PAGE_ROWS_COUNT, False)
    accounts = p.items
    pagpages = {'has_prev': p.has_prev, 'has_next': p.has_next, 'prev_num':p.prev_num, 'next_num':p.next_num}
    return render_template('accounts.html', form=form, query=query, accounts=accounts, pagpages=pagpages)


@app.route('/account/<nickname>', methods=['GET', 'POST'])
@login_required
def account(nickname):
    page = account_prev_page
    search_value = request.args.get('search_value')
    account = Account.query.filter_by(nickname=nickname).first_or_404()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Promote to admin':
            account.accounttype=3
            db.session.commit()
            return render_template('account.html', account=account)
        elif request.form['submit_button'] == 'Promote to moder':
            account.accounttype=2
            db.session.commit()
            return render_template('account.html', account=account)
        elif request.form['submit_button'] == 'Go back to accounts':
            return redirect(url_for('accounts', page=page, search_value=search_value))
        else:
            pass
    elif request.method == 'GET':
        return render_template('account.html', account=account)




@app.route('/create-account', methods=['GET', 'POST'])
@login_required
def create_account():
    form = CreateAccountForm()
    if form.validate_on_submit():
        account = Account(
            nickname=form.nickname.data,
            rank=form.rank.data,
            clanname=form.clanname.data,
            accounttype=form.accounttype.data,
        )
        db.session.add(account)
        db.session.commit()
        flash('{} account created, rank = {}, clan = {}, account type = {}'.format(form.nickname.data, form.rank.data, form.clanname.data, form.accounttype.data))
        return redirect('/create-account')
    return render_template('create-account.html', title='Create Account', form=form)
