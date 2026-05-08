from flask import Blueprint, jsonify, render_template, current_app
from flask_login import login_required, current_user
from services.analytics_service import generate_stats, generate_trend_chart
import os

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
@login_required
def analytics_page():
    # Pre-generate the trend chart image
    generate_trend_chart(current_user.id, current_app.static_folder)
    return render_template('analytics.html', trend_image=f'images/trend_{current_user.id}.png')

@analytics_bp.route('/api/analytics')
@login_required
def get_analytics():
    stats = generate_stats(current_user.id)
    return jsonify(stats), 200
