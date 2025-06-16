#app/utils/import_excel.py

import pandas as pd
from io import BytesIO
from datetime import datetime
from flask import flash
from app import db
from app.models.asset import Asset
from app.models.lifecycle import Lifecycle
from app.models.user import User

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def process_excel_import(file_stream, current_user):
    try:
        # Read Excel file into pandas DataFrame
        df = pd.read_excel(file_stream)
        
        # Validate required columns
        required_columns = ['asset_tag', 'name', 'category', 'status']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            flash(f'Missing required columns: {", ".join(missing_columns)}', 'danger')
            return False
        
        # Process each row
        success_count = 0
        error_count = 0
        for index, row in df.iterrows():
            try:
                # Convert empty strings to None
                row = row.where(pd.notnull(row), None)
                
                # Create new asset
                asset = Asset(
                    asset_tag=row['asset_tag'],
                    name=row['name'],
                    category=row['category'],
                    model=row.get('model'),
                    serial_number=row.get('serial_number'),
                    manufacturer=row.get('manufacturer'),
                    purchase_date=pd.to_datetime(row['purchase_date']).date() if row.get('purchase_date') else None,
                    purchase_cost=float(row['purchase_cost']) if row.get('purchase_cost') else None,
                    warranty_expiry=pd.to_datetime(row['warranty_expiry']).date() if row.get('warranty_expiry') else None,
                    status=row['status'],
                    location=row.get('location', 'Storage'),
                    notes=row.get('notes'),
                    created_at=datetime.utcnow()
                )
                
                # Add to database
                db.session.add(asset)
                
                # Create lifecycle event
                lifecycle = Lifecycle(
                    asset=asset,
                    event_type='Import',
                    description='Imported from Excel file',
                    user_id=current_user.id if current_user else None
                )
                db.session.add(lifecycle)
                
                success_count += 1
            except Exception as e:
                error_count += 1
                flash(f'Error processing row {index + 2}: {str(e)}', 'warning')
                continue
        
        # Commit all successful imports
        db.session.commit()
        
        flash(f'Successfully imported {success_count} assets. {error_count} failed.', 
              'success' if success_count > 0 else 'warning')
        return success_count > 0
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error processing Excel file: {str(e)}', 'danger')
        return False

def get_import_template():
    # Create a sample DataFrame with required columns
    data = {
        'asset_tag': ['ASSET-001', 'ASSET-002'],
        'name': ['Sample Laptop', 'Sample Monitor'],
        'category': ['Laptop', 'Monitor'],
        'model': ['Model X', 'Model Y'],
        'serial_number': ['SN001', 'SN002'],
        'manufacturer': ['Dell', 'HP'],
        'purchase_date': ['2023-01-15', '2023-01-20'],
        'purchase_cost': [1200.00, 300.00],
        'warranty_expiry': ['2025-01-15', '2025-01-20'],
        'status': ['Available', 'Available'],
        'location': ['Warehouse', 'Warehouse'],
        'notes': ['New device', 'Refurbished']
    }
    
    # Create Excel file in memory
    output = BytesIO()
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Assets')
    writer.save()
    output.seek(0)
    
    return output