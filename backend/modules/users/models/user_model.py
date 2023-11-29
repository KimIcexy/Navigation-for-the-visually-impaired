from sqlalchemy import Column, Integer, String, DateTime, Boolean, LargeBinary
from sqlalchemy.orm import validates
import bcrypt  # For hashing passwords
import uuid
from datetime import datetime
from deepface import DeepFace # For face verification. Will make an util for this later, rather than... well, importing it here.

from database.db import db
from utils.image import base64_to_image, image_to_base64

class User(db.Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    # Basic user information
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)

    # Other user information
    last_login = Column(DateTime)
    is_admin = Column(Boolean)
    is_active = Column(Boolean)
    date_joined = Column(DateTime)

    # Face thingy
    face_vector = Column(String)

    def __init__(self, data):
        self.id = str(uuid.uuid4())
        self.username = data['username']
        self.password = data['password']
        self.email = data['email']
        self.phone = data['phone']

        self.last_login = None
        self.is_admin = False
        self.is_active = True
        self.date_joined = datetime.utcnow()

        # Face thingy
        self.face_vector = None

    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 6, 'Password must be at least 6 characters long.'

        # Hash password
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, 'Email must be valid.'
        return email
    
    @validates('phone')
    def validate_phone(self, key, phone):
        assert len(phone) == 10 or len(phone) == 11, 'Phone number must be 10 or 11 digits long.'
        return phone

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def verify_face(self, face):
        face_1 = base64_to_image(self.face_vector)
        face_2 = base64_to_image(face)

        if face_1 is None or face_2 is None:
            return False
        
        try:
            result = DeepFace.verify(face_1, face_2, distance_metric='cosine')
        except:
            return False
        
        return result['verified']
    
    def simple_user(self):
        return {
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
        }