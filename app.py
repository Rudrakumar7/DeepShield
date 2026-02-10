from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from utils.db import db
from utils.models import User, ScanResult
from utils.ai_engine import analyze_image, analyze_audio, analyze_video
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/academy')
@login_required
def academy():
    return render_template('academy/index.html')

@app.route('/academy/learning')
@login_required
def academy_learning():
    return render_template('academy/learning_paths.html')

@app.route('/academy/careers')
@login_required
def academy_careers():
    return render_template('academy/career_guide.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Detection Routes
def handle_upload(scan_type, analyze_func):
    result = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Analyze
            analysis = analyze_func(filepath)
            
            # Save Result
            scan = ScanResult(
                filename=filename,
                scan_type=scan_type,
                result=analysis['result'],
                confidence=analysis['confidence'],
                user_id=current_user.id
            )
            db.session.add(scan)
            db.session.commit()
            
            result = analysis
            
            # Cleanup (optional, keep for demo)
            # os.remove(filepath)
            
    return result

@app.route('/detect/image', methods=['GET', 'POST'])
@login_required
def detect_image():
    result = handle_upload('image', analyze_image)
    return render_template('detect_image.html', result=result)

@app.route('/detect/audio', methods=['GET', 'POST'])
@login_required
def detect_audio():
    result = handle_upload('audio', analyze_audio)
    return render_template('detect_audio.html', result=result)

@app.route('/detect/video', methods=['GET', 'POST'])
@login_required
def detect_video():
    result = handle_upload('video', analyze_video)
    return render_template('detect_video.html', result=result)

@app.route('/tools')
@login_required
def tools():
    return render_template('tools.html')

from utils.password_utils import generate_personalized_password

@app.route('/tools/password-generator', methods=['GET', 'POST'])
@login_required
def password_generator():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', '')
        year = data.get('year', '')
        keyword = data.get('keyword', '')
        
        password = generate_personalized_password(name, year, keyword)
        return jsonify({'password': password})
        
    return render_template('tools/password_generator.html')

from utils.phishing import check_url
from flask import jsonify

@app.route('/tools/phishing-checker', methods=['GET', 'POST'])
@login_required
def phishing_checker():
    if request.method == 'POST':
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        analysis = check_url(url)
        return jsonify(analysis)
        
    return render_template('tools/phishing_checker.html')

from utils.password_strength import check_password_strength

@app.route('/tools/password-strength', methods=['GET', 'POST'])
@login_required
def password_strength():
    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password', '')
        result = check_password_strength(password)
        return jsonify(result)
        
    return render_template('tools/password_strength.html')

@app.route('/tools/phishing-simulation')
@login_required
def phishing_simulation():
    return render_template('tools/phishing_simulation.html')



from utils.news import get_cyber_news, get_mock_news

@app.route('/news')
@login_required
def cyber_news():
    try:
        news = get_cyber_news()
    except:
        news = get_mock_news()
    return render_template('news.html', news=news)

from utils.chatbot import get_bot_response

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    bot_response = get_bot_response(user_msg)
    return jsonify({'response': bot_response})

@app.route('/awareness')
def awareness():
    return render_template('awareness.html')

# Create DB Tables
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
