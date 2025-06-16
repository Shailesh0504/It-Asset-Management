#app/utils/lifecycle_helper.py

from datetime import datetime
from app import db
from app.models import Asset, Lifecycle, Transaction, User
from app.utils.decorators import commit_transaction

class LifecycleHelper:
    @staticmethod
    @commit_transaction
    def create_asset(asset_data, user_id=None):
        """
        Create a new asset with initial lifecycle event
        """
        asset = Asset(**asset_data)
        db.session.add(asset)
        
        lifecycle_event = Lifecycle(
            asset=asset,
            event_type='Creation',
            description='Asset created in system',
            user_id=user_id
        )
        db.session.add(lifecycle_event)
        
        return asset

    @staticmethod
    @commit_transaction
    def assign_asset(asset_id, user_id, assigner_id=None, due_date=None, notes=None):
        """
        Assign an asset to a user
        """
        asset = Asset.query.get_or_404(asset_id)
        user = User.query.get_or_404(user_id)
        
        # Create transaction record
        transaction = Transaction(
            asset_id=asset.id,
            user_id=user.id,
            transaction_type='checkout',
            due_date=due_date,
            notes=notes
        )
        db.session.add(transaction)
        
        # Update asset status
        asset.status = 'Assigned'
        asset.location = f"Assigned to {user.username}"
        
        # Create lifecycle event
        lifecycle_event = Lifecycle(
            asset=asset,
            event_type='Assignment',
            description=f"Assigned to {user.username}",
            user_id=assigner_id
        )
        db.session.add(lifecycle_event)
        
        return asset

    @staticmethod
    @commit_transaction
    def unassign_asset(asset_id, requester_id=None, notes=None):
        """
        Unassign/return an asset
        """
        asset = Asset.query.get_or_404(asset_id)
        
        # Get current assignment
        current_assignment = Transaction.query.filter_by(
            asset_id=asset.id,
            transaction_type='checkout'
        ).order_by(Transaction.transaction_date.desc()).first()
        
        if current_assignment:
            user = User.query.get(current_assignment.user_id)
            
            # Create checkin transaction
            transaction = Transaction(
                asset_id=asset.id,
                user_id=user.id,
                transaction_type='checkin',
                notes=notes
            )
            db.session.add(transaction)
            
            # Update asset status
            asset.status = 'Available'
            asset.location = 'Storage'
            
            # Create lifecycle event
            lifecycle_event = Lifecycle(
                asset=asset,
                event_type='Return',
                description=f"Returned from {user.username}",
                user_id=requester_id
            )
            db.session.add(lifecycle_event)
            
            return asset
        return None

    @staticmethod
    @commit_transaction
    def update_asset_status(asset_id, new_status, user_id=None, notes=None):
        """
        Update asset status (Maintenance, Retired, Lost, etc.)
        """
        asset = Asset.query.get_or_404(asset_id)
        old_status = asset.status
        asset.status = new_status
        
        # Create lifecycle event
        lifecycle_event = Lifecycle(
            asset=asset,
            event_type='Status Change',
            description=f"Status changed from {old_status} to {new_status}",
            user_id=user_id,
            notes=notes
        )
        db.session.add(lifecycle_event)
        
        return asset

    @staticmethod
    @commit_transaction
    def transfer_asset(asset_id, from_user_id, to_user_id, requester_id=None, notes=None):
        """
        Transfer asset between users
        """
        asset = Asset.query.get_or_404(asset_id)
        to_user = User.query.get_or_404(to_user_id)
        
        # Complete current assignment
        LifecycleHelper.unassign_asset(asset_id, requester_id, notes)
        
        # Create new assignment
        return LifecycleHelper.assign_asset(
            asset_id=asset_id,
            user_id=to_user_id,
            assigner_id=requester_id,
            notes=notes
        )

    @staticmethod
    def get_asset_history(asset_id, limit=None):
        """
        Get complete history for an asset
        """
        asset = Asset.query.get_or_404(asset_id)
        
        query = Lifecycle.query.filter_by(asset_id=asset.id)\
            .order_by(Lifecycle.event_date.desc())
            
        if limit:
            query = query.limit(limit)
            
        return query.all()

    @staticmethod
    def get_user_assignments(user_id):
        """
        Get all assets currently assigned to a user
        """
        return Transaction.query.filter_by(
            user_id=user_id,
            transaction_type='checkout'
        ).join(Asset).filter(
            Asset.status == 'Assigned'
        ).all()

    @staticmethod
    def generate_asset_report(asset_id):
        """
        Generate a comprehensive report for an asset
        """
        asset = Asset.query.get_or_404(asset_id)
        history = LifecycleHelper.get_asset_history(asset_id)
        assignments = Transaction.query.filter_by(asset_id=asset_id).all()
        
        return {
            'asset': asset,
            'history': history,
            'assignments': assignments,
            'current_status': asset.status,
            'current_location': asset.location,
            'warranty_status': 'Active' if asset.warranty_expiry and asset.warranty_expiry > datetime.now().date() else 'Expired'
        }


def commit_transaction(func):
    """
    Decorator to handle database commits and rollbacks
    """
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e
    return wrapper