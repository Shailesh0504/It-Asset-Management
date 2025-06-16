from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional
from datetime import date

class AssetForm(FlaskForm):
    asset_tag = StringField('Asset Tag', validators=[DataRequired()])
    name = StringField('Asset Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Tablet', 'Tablet'),
        ('Phone', 'Phone'),
        ('Monitor', 'Monitor'),
        ('Printer', 'Printer'),
        ('Server', 'Server'),
        ('Network', 'Network Equipment'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    serial_number = StringField('Serial Number', validators=[DataRequired()])
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])
    purchase_date = DateField('Purchase Date', default=date.today, validators=[DataRequired()])
    purchase_cost = FloatField('Purchase Cost', validators=[Optional()])
    warranty_expiry = DateField('Warranty Expiry', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('Available', 'Available'),
        ('Assigned', 'Assigned'),
        ('Maintenance', 'Maintenance'),
        ('Retired', 'Retired'),
        ('Lost', 'Lost')
    ], validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Asset')

class AssignAssetForm(FlaskForm):
    user_id = SelectField('Assign To', coerce=int, validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Assign Asset')