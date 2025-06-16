#app/forms/report_filter_form.py

from flask_wtf import FlaskForm
from wtforms import (SelectField, DateField, IntegerField, StringField, 
                     BooleanField, SubmitField)
from wtforms.validators import Optional, NumberRange
from datetime import date, timedelta

class AssetReportFilterForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('', 'All Statuses'),
        ('Available', 'Available'),
        ('Assigned', 'Assigned'),
        ('Maintenance', 'Maintenance'),
        ('Retired', 'Retired'),
        ('Lost', 'Lost')
    ], validators=[Optional()])
    
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Tablet', 'Tablet'),
        ('Phone', 'Phone'),
        ('Monitor', 'Monitor'),
        ('Printer', 'Printer'),
        ('Server', 'Server'),
        ('Network', 'Network Equipment'),
        ('Other', 'Other')
    ], validators=[Optional()])
    
    location = StringField('Location', validators=[Optional()])
    include_inactive = BooleanField('Include Inactive Assets', default=False)
    submit = SubmitField('Generate Report')

class WarrantyReportFilterForm(FlaskForm):
    threshold_days = IntegerField('Warn Before Expiry (Days)', 
                                default=30,
                                validators=[NumberRange(min=1, max=365)])
    
    status = SelectField('Asset Status', choices=[
        ('', 'All Statuses'),
        ('Assigned', 'Only Assigned'),
        ('Available', 'Only Available')
    ], validators=[Optional()])
    
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Tablet', 'Tablet'),
        ('Phone', 'Phone'),
        ('Server', 'Server')
    ], validators=[Optional()])
    
    submit = SubmitField('Generate Report')

class AssignmentReportFilterForm(FlaskForm):
    user = StringField('User (Username or Email)', validators=[Optional()])
    
    date_range = SelectField('Date Range', choices=[
        ('7', 'Last 7 Days'),
        ('30', 'Last 30 Days'),
        ('90', 'Last 90 Days'),
        ('365', 'Last Year'),
        ('custom', 'Custom Range')
    ], default='30')
    
    start_date = DateField('From', 
                         default=date.today() - timedelta(days=30),
                         validators=[Optional()])
    
    end_date = DateField('To', 
                       default=date.today(),
                       validators=[Optional()])
    
    include_returned = BooleanField('Include Returned Assets', default=False)
    submit = SubmitField('Generate Report')

class AuditLogFilterForm(FlaskForm):
    event_type = SelectField('Event Type', choices=[
        ('', 'All Events'),
        ('Creation', 'Asset Creation'),
        ('Assignment', 'Assignments'),
        ('Return', 'Returns'),
        ('Status Change', 'Status Changes'),
        ('Import', 'Bulk Imports'),
        ('Export', 'Exports')
    ], validators=[Optional()])
    
    user = StringField('Performed By', validators=[Optional()])
    
    date_range = SelectField('Date Range', choices=[
        ('1', 'Last 24 Hours'),
        ('7', 'Last 7 Days'),
        ('30', 'Last 30 Days'),
        ('90', 'Last 90 Days'),
        ('custom', 'Custom Range')
    ], default='7')
    
    start_date = DateField('From', 
                         default=date.today() - timedelta(days=7),
                         validators=[Optional()])
    
    end_date = DateField('To', 
                       default=date.today(),
                       validators=[Optional()])
    
    show_system = BooleanField('Include System Events', default=False)
    submit = SubmitField('Generate Report')

class CustomReportForm(FlaskForm):
    report_type = SelectField('Report Type', choices=[
        ('asset_summary', 'Asset Summary'),
        ('user_assignments', 'User Assignments'),
        ('warranty_status', 'Warranty Status'),
        ('lifecycle_history', 'Lifecycle History')
    ], validators=[Optional()])
    
    columns = SelectField('Columns', choices=[
        ('basic', 'Basic Information'),
        ('extended', 'Extended Details'),
        ('custom', 'Custom Selection')
    ], default='basic')
    
    # Dynamic field that will be populated via JavaScript
    custom_columns = StringField('Custom Columns', validators=[Optional()])
    
    format = SelectField('Export Format', choices=[
        ('html', 'Web View'),
        ('excel', 'Excel'),
        ('pdf', 'PDF')
    ], default='html')
    
    submit = SubmitField('Generate Report')