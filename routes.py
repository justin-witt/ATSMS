"""
File: routes.py
Author: Justin Wittenmeier
Description: Main file for server management tool.

Last Modified: January 1, 2024

"""
import config
from util import servermanager
from auth import authenticate, authentication, user
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

# initalize servermanager
servermanager.init_manager(exe_path=config.SERVER_EXE, data_path=config.USER_DATA_DIR, default_cfg_path=config.DEFAULT_CONFIG)

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
    return render_template('dashboard.html', servers=servermanager.get_servers(),active_servers=servermanager.get_running_servers())

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

@authentication.unauthorized_handler
def unauthorized_callbac():
    return redirect(url_for('views.login'))