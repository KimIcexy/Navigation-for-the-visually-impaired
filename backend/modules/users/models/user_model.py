import sys
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY, Float
from sqlalchemy.orm import validates
import bcrypt  # For hashing passwords
import uuid
from datetime import datetime
from deepface import DeepFace # For face verification. Will make an util for this later, rather than... well, importing it here.

from database.db import db
from utils.image import euclide_l2

class User(db.Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    # Basic user information
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    # Other user information
    last_login = Column(DateTime)
    is_admin = Column(Boolean)
    is_active = Column(Boolean)
    date_joined = Column(DateTime)

    # Face thingy
    face_vector = Column(ARRAY(Float))

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
        assert len(password) > 6, 'Mật khẩu phải dài ít nhất 6 ký tự.'

        # Hash password
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, 'Email không đúng cú pháp.'
        return email
    
    @validates('phone')
    def validate_phone(self, key, phone):
        assert len(phone) == 10 or len(phone) == 11, 'Số điện thoại phải dài 10 hoặc 11 ký tự.'
        return phone

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def verify_face(self, face):
        face_1 = self.face_vector
        face_2 = DeepFace.represent(face, detector_backend='retinaface')
        face_2 = face_2[0]['embedding']

        if face_1 is None or face_2 is None:
            return False
        
        try:
            # Compare face embeddings vectors, probably using Euclidean L2
            result = euclide_l2(face_1, face_2)
        except ValueError:
            print(sys.exc_info()[0])
            return False
        
        return result
    
    def simple_user(self):
        return {
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
        }