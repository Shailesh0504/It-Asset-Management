from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.asset import Asset
from app.models.user import User
from app.models.transaction import Transaction

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
def dashboard():
    total_assets = Asset.query.count()
    total_users = User.query.count()
    available_assets = Asset.query.filter_by(status='Available').count()
    recent_transactions = Transaction.query.order_by(Transaction.transaction_date.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         total_assets=total_assets,
                         total_users=total_users,
                         available_assets=available_assets,
                         recent_transactions=recent_transactions)