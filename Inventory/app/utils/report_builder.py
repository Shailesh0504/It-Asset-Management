#app/utils/report_builder.py

import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
from flask import send_file
from app import db
from app.models import Asset, User, Transaction, Lifecycle
from app.utils.export_excel import generate_excel_output

class ReportBuilder:
    @staticmethod
    def generate_asset_status_report(status=None):
        """
        Generate a report of assets filtered by status
        """
        query = Asset.query
        
        if status:
            query = query.filter_by(status=status)
            
        assets = query.order_by(Asset.asset_tag).all()
        
        report_data = []
        for asset in assets:
            last_transaction = Transaction.query.filter_by(asset_id=asset.id)\
                .order_by(Transaction.transaction_date.desc()).first()
                
            assigned_to = last_transaction.user.username if last_transaction and \
                last_transaction.transaction_type == 'checkout' else 'N/A'
                
            report_data.append({
                'Asset Tag': asset.asset_tag,
                'Name': asset.name,
                'Category': asset.category,
                'Status': asset.status,
                'Location': asset.location,
                'Assigned To': assigned_to,
                'Purchase Date': asset.purchase_date.strftime('%Y-%m-%d') if asset.purchase_date else 'N/A',
                'Warranty Expiry': asset.warranty_expiry.strftime('%Y-%m-%d') if asset.warranty_expiry else 'N/A',
                'Last Updated': asset.updated_at.strftime('%Y-%m-%d %H:%M') if asset.updated_at else 'N/A'
            })
        
        return report_data

    @staticmethod
    def generate_warranty_report(threshold_days=30):
        """
        Generate a report of assets with expiring warranties
        """
        today = datetime.now().date()
        assets = Asset.query.filter(
            Asset.warranty_expiry.isnot(None)
            .order_by(Asset.warranty_expiry).all())
        
        report_data = []
        for asset in assets:
            days_remaining = (asset.warranty_expiry - today).days
            if days_remaining <= threshold_days:
                report_data.append({
                    'Asset Tag': asset.asset_tag,
                    'Name': asset.name,
                    'Category': asset.category,
                    'Warranty Expiry': asset.warranty_expiry.strftime('%Y-%m-%d'),
                    'Days Remaining': days_remaining,
                    'Status': asset.status,
                    'Assigned To': Transaction.query.filter_by(
                        asset_id=asset.id,
                        transaction_type='checkout'
                    ).order_by(Transaction.transaction_date.desc()).first().user.username if asset.status == 'Assigned' else 'N/A'
                })
        
        return report_data

    @staticmethod
    def generate_user_assignment_report(user_id=None):
        """
        Generate a report of user assignments
        """
        query = db.session.query(
            User.username,
            Asset.asset_tag,
            Asset.name,
            Asset.category,
            Transaction.transaction_date,
            Transaction.due_date
        ).join(
            Transaction, Transaction.user_id == User.id
        ).join(
            Asset, Asset.id == Transaction.asset_id
        ).filter(
            Transaction.transaction_type == 'checkout',
            Asset.status == 'Assigned'
        )
        
        if user_id:
            query = query.filter(User.id == user_id)
            
        assignments = query.order_by(User.username, Asset.asset_tag).all()
        
        report_data = []
        for assignment in assignments:
            report_data.append({
                'Username': assignment.username,
                'Asset Tag': assignment.asset_tag,
                'Asset Name': assignment.name,
                'Category': assignment.category,
                'Assignment Date': assignment.transaction_date.strftime('%Y-%m-%d'),
                'Due Date': assignment.due_date.strftime('%Y-%m-%d') if assignment.due_date else 'N/A'
            })
        
        return report_data

    @staticmethod
    def generate_asset_history_report(asset_id):
        """
        Generate a detailed history report for a specific asset
        """
        asset = Asset.query.get_or_404(asset_id)
        history = Lifecycle.query.filter_by(asset_id=asset.id)\
            .order_by(Lifecycle.event_date.desc()).all()
        
        report_data = []
        for event in history:
            report_data.append({
                'Event Date': event.event_date.strftime('%Y-%m-%d %H:%M'),
                'Event Type': event.event_type,
                'Description': event.description,
                'Performed By': User.query.get(event.user_id).username if event.user_id else 'System',
                'Notes': event.notes or 'N/A'
            })
        
        return {
            'asset': {
                'Asset Tag': asset.asset_tag,
                'Name': asset.name,
                'Current Status': asset.status,
                'Location': asset.location
            },
            'history': report_data
        }

    @staticmethod
    def generate_audit_log_report(days=30):
        """
        Generate a system audit log report
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        events = Lifecycle.query.filter(
            Lifecycle.event_date >= cutoff_date
        ).order_by(Lifecycle.event_date.desc()).all()
        
        report_data = []
        for event in events:
            asset = Asset.query.get(event.asset_id)
            report_data.append({
                'Timestamp': event.event_date.strftime('%Y-%m-%d %H:%M'),
                'Asset Tag': asset.asset_tag if asset else 'N/A',
                'Event Type': event.event_type,
                'Description': event.description,
                'User': User.query.get(event.user_id).username if event.user_id else 'System',
                'Notes': event.notes or 'N/A'
            })
        
        return report_data

    @staticmethod
    def export_to_excel(report_data, sheet_name='Report'):
        """
        Export report data to Excel format
        """
        if not report_data:
            return None
            
        # Handle nested report structures
        if isinstance(report_data, dict) and 'history' in report_data:
            # Asset history report format
            df_main = pd.DataFrame([report_data['asset']])
            df_history = pd.DataFrame(report_data['history'])
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_main.to_excel(writer, sheet_name='Asset Details', index=False)
                df_history.to_excel(writer, sheet_name='History', index=False)
            output.seek(0)
        else:
            # Standard flat report format
            df = pd.DataFrame(report_data)
            output = generate_excel_output(df, sheet_name)
        
        return output

    @staticmethod
    def send_excel_response(report_data, filename, sheet_name='Report'):
        """
        Generate and send an Excel file response
        """
        excel_file = ReportBuilder.export_to_excel(report_data, sheet_name)
        if not excel_file:
            return None
            
        return send_file(
            excel_file,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )