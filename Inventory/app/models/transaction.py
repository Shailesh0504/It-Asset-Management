from datetime import datetime
from app import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'checkout', 'checkin', 'transfer'
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    # Relationships
    asset = db.relationship('Asset', back_populates='assigned_to')
    user = db.relationship('User', back_populates='transactions')

    def __repr__(self):
        return f'<Transaction {self.transaction_type} of asset {self.asset_id} to user {self.user_id}>'