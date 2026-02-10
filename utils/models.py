from datetime import datetime
from flask_login import UserMixin
from .db import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to scans
    scans = db.relationship('ScanResult', backref='author', lazy=True)

class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    scan_type = db.Column(db.String(20), nullable=False) # 'image', 'audio', 'video'
    result = db.Column(db.String(20), nullable=False)    # 'Real' or 'Fake'
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'scan_type': self.scan_type,
            'result': self.result,
            'confidence': self.confidence,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
