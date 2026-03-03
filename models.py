"""
Database models for Accident Hospital Service
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(500))
    ambulance_available = db.Column(db.Integer, default=0)
    emergency_beds = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'ambulance_available': self.ambulance_available,
            'emergency_beds': self.emergency_beds
        }


class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    incident_type = db.Column(db.String(50))  # 'crash', 'manual_report', 'ai_detection'
    severity = db.Column(db.String(50))  # 'low', 'medium', 'high', 'critical'
    confidence = db.Column(db.Float)  # AI confidence score
    sensor_data = db.Column(db.JSON)  # Acceleration, gyro data
    image_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    status = db.Column(db.String(50), default='reported')  # reported, dispatched, arrived, resolved
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'incident_type': self.incident_type,
            'severity': self.severity,
            'confidence': self.confidence,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'hospital_id': self.hospital_id
        }


class IncidentAlert(db.Model):
    __tablename__ = 'incident_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    alert_type = db.Column(db.String(50))  # 'sms', 'email', 'app_notification'
    sent = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime)
    response_status = db.Column(db.String(50))  # 'pending', 'accepted', 'rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'hospital_id': self.hospital_id,
            'alert_type': self.alert_type,
            'sent': self.sent,
            'response_status': self.response_status
        }
