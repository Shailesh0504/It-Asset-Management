from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models.asset import Asset
from app.models.transaction import Transaction
from app.forms.asset_forms import AssetForm, AssignAssetForm

bp = Blueprint('asset', __name__)

@bp.route('/assets')
@login_required
def list_assets():
    page = request.args.get('page', 1, type=int)
    assets = Asset.query.order_by(Asset.asset_tag).paginate(page=page, per_page=10)
    return render_template('assets/view_assets.html', assets=assets)

@bp.route('/assets/add', methods=['GET', 'POST'])
@login_required
def add_asset():
    form = AssetForm()
    if form.validate_on_submit():
        asset = Asset(
            asset_tag=form.asset_tag.data,
            name=form.name.data,
            category=form.category.data,
            model=form.model.data,
            serial_number=form.serial_number.data,
            manufacturer=form.manufacturer.data,
            purchase_date=form.purchase_date.data,
            purchase_cost=form.purchase_cost.data,
            warranty_expiry=form.warranty_expiry.data,
            status=form.status.data,
            location=form.location.data,
            notes=form.notes.data
        )
        db.session.add(asset)
        db.session.commit()
        flash('Asset added successfully!', 'success')
        return redirect(url_for('asset.list_assets'))
    
    return render_template('assets/add_asset.html', title='Add Asset', form=form)

# Additional routes for edit, delete, view details would follow similar patterns