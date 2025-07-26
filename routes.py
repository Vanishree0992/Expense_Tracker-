from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_user, login_required, logout_user, current_user
from extensions import db, login_manager, scheduler
from models import User, Transaction, Category, Account, Budget
from forms import LoginForm, RegisterForm, TransactionForm
from utils import save_receipt, export_transactions, check_alerts

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@main.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password_hash=form.password.data)
        db.session.add(user); db.session.commit()
        flash('Registered!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password_hash == form.password.data:
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    txns = Transaction.query.filter_by(account_id=current_user.id).all()
    categories = Category.query.all()
    return render_template('transactions.html', transactions=txns, categories=categories)

@main.route('/transaction/new', methods=['GET','POST'])
@login_required
def new_transaction():
    form = TransactionForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    form.account.choices = [(a.id, a.name) for a in Account.query.filter_by(owner_id=current_user.id).all()]
    if form.validate_on_submit():
        filename = save_receipt(form.receipt.data) if form.receipt.data else None
        txn = Transaction(amount=form.amount.data, currency=form.currency.data,
                          date=form.date.data, description=form.description.data,
                          recurring=form.recurring.data, receipt_file=filename,
                          category_id=form.category.data, account_id=form.account.data)
        db.session.add(txn); db.session.commit()
        flash('Transaction added.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('transactions.html', form=form)

@main.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@main.route('/export')
@login_required
def export():
    path = export_transactions(current_user.id)
    return send_file(path, as_attachment=True)

# Schedule alerts
scheduler.add_job(func=lambda: check_alerts(), trigger="interval", hours=1)
scheduler.start()
