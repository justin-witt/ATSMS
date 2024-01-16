"""
File: routes.py
Author: Justin Wittenmeier
Description: Main file for server management tool.

Last Modified: January 16, 2024

"""
import json
from util import servermanager
from config import DEBUG
from auth import authenticate, authentication, user
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, abort
from flask_login import login_required, login_user, logout_user, current_user

# views_bp: Blueprint for website pages or views
views_bp = Blueprint('views', __name__, template_folder='templates',static_folder='static')

@views_bp.route('/', methods=['GET', 'POST'])
@views_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    if current_user.is_authenticated:
        # Redirect to dashboard if already logged in
        return redirect(url_for('views.dashboard')) 

    if request.method == 'POST':
        password = request.form['password']

        authenticated = authenticate(password)

        if authenticated:
            # Mark user as logged in
            login_user(user)
            # Redirect to the dashboard upon successful login
            return redirect(url_for('views.dashboard')) 

        flash('Login failed. Please try again.', 'error')

    return render_template('login.html')

@views_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('views.login'))

@views_bp.route('/dashboard')
@login_required
def dashboard():
    # Logic for dashboard view
    return render_template('dashboard.html', servers=servermanager.get_servers(), active_servers=servermanager.get_running_servers())

@views_bp.route('/edit/<server_id>', methods=['GET', 'POST'])
@login_required
def edit_server(server_id):
    # Logic for editing a server configuration
    if request.method == 'POST':
        data = request.form['config-content']
        servermanager.edit_server(server_id, data)
        return redirect(url_for('views.dashboard'))
    data = servermanager.get_cfg(server_id)
    return render_template('edit.html', data=data, server_id=server_id)

@views_bp.route('/create')
@login_required
def create_server():
    # Logic for creating a new server
    server_id = servermanager.create_server()
    return redirect(url_for('views.edit_server', server_id=server_id))

@views_bp.route('/delete/<server_id>')
@login_required
def delete_server(server_id):
    # Logic for deleting a server
    servermanager.delete_server(server_id)
    return redirect(url_for('views.dashboard'))

@views_bp.route('/handler/<server_id>/<action>')
@login_required
def handler(server_id, action):
    # Logic for handling server actions
    if action == 'start':
        servermanager.start_server(server_id)
    elif action == 'stop':
        servermanager.stop_server(server_id)
    else:
        return redirect(url_for())
    return redirect(url_for('views.dashboard'))

#Added in v0.1.1
@views_bp.route('/player_count/<server_id>')
@login_required
def player_count(server_id):
    return json.dumps([servermanager.get_player_count(server_id)])

#Added in v0.1.1
@views_bp.route('/reset/<server_id>')
@login_required
def reset(server_id):
    servermanager.reset_cfg(server_id)
    return redirect(url_for('views.edit_server', server_id=server_id))

#Added in v0.1.1
@views_bp.route('/logs/<server_id>')
@login_required
def logs(server_id):
    data = servermanager.get_logs(server_id, limit=500)
    return render_template('logs.html', server_name=servermanager.get_server_name(servermanager.get_cfg(server_id)), server_id=server_id, data=data)

#Added in v0.1.3
@views_bp.route('/download/<file_type>/<server_id>')
def download(file_type, server_id):
    
    #might consider putting this in a match case or something
    if file_type == 'log':
        return send_file(servermanager.log_path(server_id), as_attachment=True)
    
    #retrun error if invalid request
    return abort(400, 'Invalid request')

#Exception and unauthorized handler
#set in if statment to assist with debugging and testing (added in v0.1.2)
if not DEBUG:
    @views_bp.app_errorhandler(Exception)
    def handle_error(e):
        return render_template('error.html', error=e), 500

#AUTHENTICATION REDIRECT DO NOT TOUCH THIS
@authentication.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('views.login'))