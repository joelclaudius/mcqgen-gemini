from datetime import datetime
import uuid
from extensions import db  # Move this import to the top

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    api_key = db.Column(db.String(120), unique=True, nullable=True)  # API key is initially None
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to access all documents created by the user
    documents = db.relationship('Document', backref='user', lazy=True)

    def generate_api_key(self):
        return str(uuid.uuid4())  # Generate a unique API key

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    docx_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key to reference the user who created the document
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



class ApiRequestLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(120), nullable=False)
    processing_time = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ApiRequestLog {self.endpoint} - {self.processing_time}ms>"