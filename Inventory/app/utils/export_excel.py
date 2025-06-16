import pandas as pd
from io import BytesIO
from flask import send_file
from app.models.asset import Asset

def export_assets_to_excel():
    # Query all assets
    assets = Asset.query.all()
    
    # Create a DataFrame
    data = {
        'Asset Tag': [a.asset_tag for a in assets],
        'Name': [a.name for a in assets],
        'Category': [a.category for a in assets],
        'Model': [a.model for a in assets],
        'Serial Number': [a.serial_number for a in assets],
        'Status': [a.status for a in assets],
        'Location': [a.location for a in assets],
        'Purchase Date': [a.purchase_date.strftime('%Y-%m-%d') if a.purchase_date else '' for a in assets],
        'Purchase Cost': [a.purchase_cost for a in assets],
        'Warranty Expiry': [a.warranty_expiry.strftime('%Y-%m-%d') if a.warranty_expiry else '' for a in assets]
    }
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Assets')
    writer.save()
    output.seek(0)
    
    return output