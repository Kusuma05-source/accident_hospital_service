"""
Accident Hospital Service - Main Flask Application
End-to-end accident detection and hospital emergency response system
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from config import *
from models import db, Hospital, Incident, IncidentAlert
from utils import AccidentDetector, HospitalFinder, AlertService

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize database
db.init_app(app)
CORS(app)

# Create uploads directory
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ==================== Database Initialization ====================

@app.before_request
def init_db():
    """Initialize database on first request"""
    if not hasattr(app, 'db_initialized'):
        with app.app_context():
            db.create_all()
            
            # Add sample hospitals if none exist
            if Hospital.query.first() is None:
                sample_hospitals = [
                    Hospital(
                        name='City Medical Center',
                        phone='+1-555-0101',
                        email='emergency@citymedical.com',
                        latitude=40.7128,
                        longitude=-74.0060,
                        address='123 Main St, Downtown',
                        ambulance_available=3,
                        emergency_beds=8
                    ),
                    Hospital(
                        name='St. Johns Hospital',
                        phone='+1-555-0102',
                        email='alert@stjohns.com',
                        latitude=40.7580,
                        longitude=-73.9855,
                        address='456 Oak Ave, Midtown',
                        ambulance_available=2,
                        emergency_beds=5
                    ),
                    Hospital(
                        name='General Emergency Clinic',
                        phone='+1-555-0103',
                        email='emergency@generalclinic.com',
                        latitude=40.7489,
                        longitude=-73.9680,
                        address='789 Elm Rd, East Side',
                        ambulance_available=4,
                        emergency_beds=10
                    )
                ]
                for hospital in sample_hospitals:
                    db.session.add(hospital)
                db.session.commit()
            
            app.db_initialized = True


# ==================== Home & Location Routes ====================

@app.route("/")
def home():
    """Main dashboard"""
    return render_template("index.html")


@app.route("/api/location", methods=["POST"])
def update_location():
    """Update user location"""
    try:
        data = request.get_json()
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        accuracy = data.get("accuracy")
        
        return jsonify({
            "success": True,
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": accuracy,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


# ==================== Nearest Hospitals Routes ====================

@app.route("/nearest-hospitals", methods=["GET", "POST"])
def nearest_hospitals():
    """Get nearest hospitals"""
    try:
        if request.method == "POST":
            data = request.get_json()
            latitude = data.get("latitude")
            longitude = data.get("longitude")
        else:
            latitude = request.args.get("latitude", type=float)
            longitude = request.args.get("longitude", type=float)
        
        if not latitude or not longitude:
            return jsonify({"error": "Latitude and longitude required"}), 400
        
        hospitals = HospitalFinder.find_nearest_hospitals(latitude, longitude)
        
        return jsonify({
            "success": True,
            "user_location": {"latitude": latitude, "longitude": longitude},
            "hospitals": hospitals,
            "count": len(hospitals)
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== Accident Detection Routes ====================

@app.route("/api/report-accident", methods=["POST"])
def report_accident():
    """Manual accident report"""
    try:
        data = request.get_json()
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        description = data.get("description", "Manual report")
        
        # Create incident
        incident = Incident(
            latitude=latitude,
            longitude=longitude,
            incident_type='manual_report',
            severity='high',
            status='reported',
            notes=description
        )
        db.session.add(incident)
        db.session.commit()
        
        # Find and alert nearest hospitals
        hospitals = HospitalFinder.find_nearest_hospitals(latitude, longitude)
        for hospital in hospitals[:3]:  # Alert top 3 nearest
            AlertService.send_alert(incident.id, hospital['id'], 'sms')
        
        return jsonify({
            "success": True,
            "incident_id": incident.id,
            "message": f"Accident reported! {len(hospitals)} hospitals alerted.",
            "hospitals": hospitals
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/sensor-crash-detect", methods=["POST"])
def detect_crash_sensors():
    """Detect crash from smartphone sensor data"""
    try:
        data = request.get_json()
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        acceleration = data.get("acceleration", [0, 0, 0])  # x, y, z
        gyroscope = data.get("gyroscope", [0, 0, 0])  # x, y, z
        
        # Detect crash
        is_crash, severity, confidence = AccidentDetector.detect_crash_from_sensors(
            acceleration, gyroscope
        )
        
        if is_crash:
            # Create incident
            incident = Incident(
                latitude=latitude,
                longitude=longitude,
                incident_type='crash',
                severity=severity,
                confidence=confidence,
                sensor_data={
                    'acceleration': acceleration,
                    'gyroscope': gyroscope
                },
                status='reported'
            )
            db.session.add(incident)
            db.session.commit()
            
            # Find and alert nearest hospitals
            hospitals = HospitalFinder.find_nearest_hospitals(latitude, longitude)
            for hospital in hospitals[:5]:  # Alert top 5
                AlertService.send_alert(incident.id, hospital['id'], 'sms')
            
            return jsonify({
                "crash_detected": True,
                "incident_id": incident.id,
                "severity": severity,
                "confidence": round(confidence * 100, 2),
                "hospitals_alerted": len(hospitals),
                "nearest_hospital": hospitals[0] if hospitals else None
            })
        
        return jsonify({
            "crash_detected": False,
            "message": "No crash detected"
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/video-crash-detect", methods=["POST"])
def detect_crash_video():
    """Detect crash from video file"""
    try:
        if 'video' not in request.files:
            return jsonify({"error": "No video file provided"}), 400
        
        video_file = request.files['video']
        latitude = request.form.get('latitude', type=float)
        longitude = request.form.get('longitude', type=float)
        
        if not video_file or not latitude or not longitude:
            return jsonify({"error": "Missing video, latitude, or longitude"}), 400
        
        # Save video
        filename = secure_filename(video_file.filename)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], timestamp + filename)
        video_file.save(filepath)
        
        # Detect crash
        detected, confidence, frames = AccidentDetector.detect_crash_from_video(filepath)
        
        response = {
            "video_processed": True,
            "crash_detected": detected,
            "confidence": round(confidence * 100, 2),
            "video_file": os.path.basename(filepath)
        }
        
        if detected:
            # Create incident
            incident = Incident(
                latitude=latitude,
                longitude=longitude,
                incident_type='ai_detection',
                severity='high' if confidence > 0.7 else 'medium',
                confidence=confidence,
                video_url=f"/uploads/{os.path.basename(filepath)}",
                status='reported'
            )
            db.session.add(incident)
            db.session.commit()
            
            # Find and alert nearest hospitals
            hospitals = HospitalFinder.find_nearest_hospitals(latitude, longitude)
            for hospital in hospitals[:5]:
                AlertService.send_alert(incident.id, hospital['id'], 'sms')
            
            response.update({
                "incident_id": incident.id,
                "hospitals_alerted": len(hospitals),
                "nearest_hospital": hospitals[0] if hospitals else None
            })
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== Incident Management Routes ====================

@app.route("/api/incidents", methods=["GET"])
def get_incidents():
    """Get all incidents"""
    try:
        incidents = Incident.query.order_by(Incident.created_at.desc()).limit(50).all()
        return jsonify({
            "success": True,
            "incidents": [inc.to_dict() for inc in incidents],
            "count": len(incidents)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/incident/<int:incident_id>", methods=["GET", "PUT"])
def manage_incident(incident_id):
    """Get or update incident details"""
    try:
        incident = Incident.query.get(incident_id)
        if not incident:
            return jsonify({"error": "Incident not found"}), 404
        
        if request.method == "GET":
            return jsonify({
                "success": True,
                "incident": incident.to_dict()
            })
        
        elif request.method == "PUT":
            data = request.get_json()
            incident.status = data.get("status", incident.status)
            incident.hospital_id = data.get("hospital_id", incident.hospital_id)
            incident.notes = data.get("notes", incident.notes)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "incident": incident.to_dict()
            })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== Hospital Management Routes ====================

@app.route("/api/hospitals", methods=["GET"])
def get_hospitals():
    """Get all hospitals"""
    try:
        hospitals = Hospital.query.all()
        return jsonify({
            "success": True,
            "hospitals": [h.to_dict() for h in hospitals],
            "count": len(hospitals)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/hospital/<int:hospital_id>", methods=["GET"])
def get_hospital(hospital_id):
    """Get hospital details"""
    try:
        hospital = Hospital.query.get(hospital_id)
        if not hospital:
            return jsonify({"error": "Hospital not found"}), 404
        
        return jsonify({
            "success": True,
            "hospital": hospital.to_dict()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== File Serving ====================

@app.route('/uploads/<filename>')
def download_file(filename):
    """Serve uploaded files"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath)
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== Health Check ====================

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Accident Hospital Service",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    })


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)