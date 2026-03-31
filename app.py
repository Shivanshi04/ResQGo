import os
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, EmergencyLog
from ml_engine import classifier
from sqlalchemy import func


app = Flask(__name__)
app.config['SECRET_KEY'] = 'safety_first_2024_secure_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safety_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize Database
with app.app_context():
    db.create_all()
    # Create an admin if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin', 
            password=generate_password_hash('admin123'), 
            email='admin@safety.com', 
            role='admin', 
            region='Central',
            family_contact='911'
        )
        db.session.add(admin)
        db.session.commit()

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        role = request.form.get('role')
        region = request.form.get('region')
        family_contact = request.form.get('family_contact')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            role=role,
            region=region,
            family_contact=family_contact
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'volunteer':
                return redirect(url_for('volunteer_dashboard'))
            return redirect(url_for('user_dashboard'))
        
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- Dashboards ---

@app.route('/dashboard/user')
@login_required
def user_dashboard():
    if current_user.role != 'user':
        return redirect(url_for('index'))
    logs = EmergencyLog.query.filter_by(user_id=current_user.id).order_by(EmergencyLog.timestamp.desc()).all()
    return render_template('user_dashboard.html', logs=logs)

@app.route('/dashboard/volunteer')
@login_required
def volunteer_dashboard():
    if current_user.role != 'volunteer':
        return redirect(url_for('index'))
    # Only see logs from their own region
    logs = EmergencyLog.query.filter_by(region=current_user.region).order_by(EmergencyLog.timestamp.desc()).all()
    return render_template('volunteer_dashboard.html', logs=logs)

@app.route('/dashboard/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    return render_template('admin_dashboard.html')

# --- Logic ---

@app.route('/trigger_sos', methods=['POST'])
@login_required
def trigger_sos():
    description = request.form.get('description', '')
    classification = classifier.classify(description)
    
    new_log = EmergencyLog(
        user_id=current_user.id,
        username=current_user.username,
        emergency_type=classification,
        description=description if description else "Manual SOS Triggered",
        region=current_user.region,
        status='Pending'
    )
    db.session.add(new_log)
    db.session.commit()
    
    flash(f'SOS ALERT SENT! AI Classified as: {classification}. Family and Volunteers notified.', 'danger')
    return redirect(url_for('user_dashboard'))

@app.route('/resolve_emergency/<int:log_id>', methods=['POST'])
@login_required
def resolve_emergency(log_id):
    if current_user.role not in ['volunteer', 'admin']:
        return redirect(url_for('index'))
    
    log = EmergencyLog.query.get(log_id)
    if log:
        log.status = 'Resolved'
        db.session.commit()
        flash('Emergency marked as resolved.')
    return redirect(request.referrer)

# --- API for Charts ---

@app.route('/api/stats')
@login_required
def get_stats():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Emergency types distribution
    type_counts = db.session.query(EmergencyLog.emergency_type, func.count(EmergencyLog.id)).group_by(EmergencyLog.emergency_type).all()
    # Region distribution
    region_counts = db.session.query(EmergencyLog.region, func.count(EmergencyLog.id)).group_by(EmergencyLog.region).all()
    
    return jsonify({
        'types': {k: v for k, v in type_counts},
        'regions': {k: v for k, v in region_counts}
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))




