from datetime import datetime
from app import db

class Lifecycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    event_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    asset = db.relationship('Asset', back_populates='lifecycle_events')
    user = db.relationship('User')

    def __repr__(self):
        return f'<Lifecycle event {self.event_type} for asset {self.asset_id}>'