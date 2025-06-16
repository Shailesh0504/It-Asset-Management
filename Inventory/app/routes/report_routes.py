from flask import render_template, send_file, Blueprint
from flask_login import login_required
from app.models.asset import Asset
from app.utils.export_excel import export_assets_to_excel

bp = Blueprint('report', __name__)

@bp.route('/reports')
@login_required
def index():
    return render_template('reports/report_dashboard.html')

@bp.route('/reports/assets')
@login_required
def asset_report():
    assets = Asset.query.order_by(Asset.asset_tag).all()
    return render_template('reports/report_detail.html', assets=assets)

@bp.route('/reports/export/assets')
@login_required
def export_assets():
    excel_file = export_assets_to_excel()
    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='assets_export.xlsx'
    )