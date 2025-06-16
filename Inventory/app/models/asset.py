from datetime import datetime
from app import db

class Asset(db.Model):
    __tablename__ = 'asset'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(50), unique=True)
    manufacturer = db.Column(db.String(100))
    purchase_date = db.Column(db.Date)
    purchase_cost = db.Column(db.Float)
    warranty_expiry = db.Column(db.Date)
    status = db.Column(db.String(20), default='Available')
    location = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assigned_to = db.relationship('Transaction', back_populates='asset', lazy=True)
    lifecycle_events = db.relationship('Lifecycle', back_populates='asset', lazy=True)

    def __repr__(self):
        return f'<Asset {self.asset_tag} - {self.name}>'