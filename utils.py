import os
from flask import current_app
from werkzeug.utils import secure_filename
import pandas as pd
from models import Transaction

def save_receipt(uploaded):
    fn = secure_filename(uploaded.filename)
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], fn)
    uploaded.save(path)
    return fn

def export_transactions(user_id):
    txns = Transaction.query.filter_by(account_id=user_id).all()
    data = [{
        'date': t.date, 'amount': t.amount, 'currency': t.currency,
        'description': t.description, 'category': t.category.name
    } for t in txns]
    df = pd.DataFrame(data)
    path = os.path.join(current_app.config['EXPORT_FOLDER'], 'export.xlsx')
    df.to_excel(path, index=False)
    return path

def check_alerts():
    # Placeholder: You can inspect budgets vs spending and send alerts.
    print("Checking budget alerts...")
