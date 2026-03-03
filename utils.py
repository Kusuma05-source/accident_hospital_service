"""
Utility functions for accident detection and hospital operations
"""
import math
import requests
import cv2
import numpy as np
from config import GOOGLE_MAPS_API_KEY, ACCELERATION_THRESHOLD, GYRO_THRESHOLD, SEARCH_RADIUS_KM
from models import Hospital, Incident, db

class AccidentDetector:
    """Detects accidents using sensor data and computer vision"""
    
    @staticmethod
    def detect_crash_from_sensors(acceleration_data, gyro_data):
        """
        Detect crash based on smartphone sensor data
        Returns: (is_crash: bool, severity: str, confidence: float)
        """
        acc_magnitude = math.sqrt(sum(x**2 for x in acceleration_data))
        gyro_magnitude = math.sqrt(sum(x**2 for x in gyro_data))
        
        # Calculate if it's a crash based on thresholds
        acc_crash = acc_magnitude > ACCELERATION_THRESHOLD
        gyro_crash = gyro_magnitude > GYRO_THRESHOLD
        
        if acc_crash or gyro_crash:
            # Calculate severity
            acc_ratio = min(acc_magnitude / (ACCELERATION_THRESHOLD * 2), 1.0)
            gyro_ratio = min(gyro_magnitude / (GYRO_THRESHOLD * 2), 1.0)
            
            confidence = (acc_ratio + gyro_ratio) / 2
            
            if confidence > 0.8:
                severity = 'critical'
            elif confidence > 0.6:
                severity = 'high'
            elif confidence > 0.4:
                severity = 'medium'
            else:
                severity = 'low'
            
            return True, severity, confidence
        
        return False, None, 0.0
    
    @staticmethod
    def detect_crash_from_video(video_path):
        """
        Detect crash in video using computer vision
        Returns: (detected: bool, confidence: float, frames_with_detection: list)
        """
        try:
            cap = cv2.VideoCapture(video_path)
            detected_frames = []
            detection_count = 0
            total_frames = 0
            
            # Process every 5th frame for efficiency
            frame_skip = 5
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                total_frames += 1
                if total_frames % frame_skip != 0:
                    continue
                
                # Simple detection: Look for sudden brightness changes or motion
                # This is a basic implementation - production would use ML model
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect edges (potential impact indicators)
                edges = cv2.Canny(gray, 100, 200)
                edge_density = np.sum(edges) / (edges.shape[0] * edges.shape[1])
                
                if edge_density > 0.15:  # Threshold for edge density
                    detection_count += 1
                    detected_frames.append(total_frames)
            
            cap.release()
            
            if detection_count > 0:
                confidence = min(detection_count / (total_frames / frame_skip), 1.0)
                if confidence > 0.3:
                    return True, confidence, detected_frames[:5]  # Return first 5 detections
            
            return False, 0.0, []
            
        except Exception as e:
            print(f"Video processing error: {e}")
            return False, 0.0, []


class HospitalFinder:
    """Find nearby hospitals using Google Maps API"""
    
    @staticmethod
    def find_nearest_hospitals(latitude, longitude, radius_km=SEARCH_RADIUS_KM):
        """
        Find nearest hospitals using Google Maps Places API
        Returns: list of hospital data
        """
        try:
            # First try to get from database (cached)
            hospitals = Hospital.query.all()
            
            if hospitals:
                # Calculate distance and sort
                hospitals_with_distance = []
                for h in hospitals:
                    distance = HospitalFinder._calculate_distance(
                        latitude, longitude, h.latitude, h.longitude
                    )
                    if distance <= radius_km:
                        hospitals_with_distance.append({
                            **h.to_dict(),
                            'distance_km': round(distance, 2)
                        })
                
                # Sort by distance
                hospitals_with_distance.sort(key=lambda x: x['distance_km'])
                return hospitals_with_distance[:5]  # Top 5 closest
        
        except Exception as e:
            print(f"Database query error: {e}")
        
        # Fallback to Google Maps API if no cached data
        if not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == 'YOUR_GOOGLE_MAPS_API_KEY_HERE':
            # Return sample data if API key not configured
            return HospitalFinder._get_sample_hospitals()
        
        try:
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                'location': f"{latitude},{longitude}",
                'radius': radius_km * 1000,
                'type': 'hospital',
                'key': GOOGLE_MAPS_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            hospitals = []
            if data['status'] == 'OK':
                for place in data['results'][:5]:  # Top 5
                    hospitals.append({
                        'name': place['name'],
                        'latitude': place['geometry']['location']['lat'],
                        'longitude': place['geometry']['location']['lng'],
                        'address': place.get('vicinity', 'N/A'),
                        'distance_km': round(
                            HospitalFinder._calculate_distance(
                                latitude, longitude,
                                place['geometry']['location']['lat'],
                                place['geometry']['location']['lng']
                            ), 2
                        ),
                        'phone': place.get('formatted_phone_number', 'N/A'),
                        'website': place.get('website', '')
                    })
            
            return hospitals
        
        except Exception as e:
            print(f"Google Maps API error: {e}")
            return HospitalFinder._get_sample_hospitals()
    
    @staticmethod
    def _calculate_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat/2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    @staticmethod
    def _get_sample_hospitals():
        """Return sample hospitals for development/demo"""
        return [
            {
                'name': 'City Medical Center',
                'phone': '+1-555-0101',
                'address': '123 Main St, Downtown',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'distance_km': 0.5,
                'ambulance_available': 3,
                'emergency_beds': 8
            },
            {
                'name': 'St. Johns Hospital',
                'phone': '+1-555-0102',
                'address': '456 Oak Ave, Midtown',
                'latitude': 40.7580,
                'longitude': -73.9855,
                'distance_km': 1.2,
                'ambulance_available': 2,
                'emergency_beds': 5
            },
            {
                'name': 'General Emergency Clinic',
                'phone': '+1-555-0103',
                'address': '789 Elm Rd, East Side',
                'latitude': 40.7489,
                'longitude': -73.9680,
                'distance_km': 1.8,
                'ambulance_available': 4,
                'emergency_beds': 10
            }
        ]


class AlertService:
    """Send alerts to hospitals and authorities"""
    
    @staticmethod
    def send_alert(incident_id, hospital_id, alert_type='sms'):
        """
        Send alert to hospital
        alert_type: 'sms', 'email', or 'api_notification'
        """
        try:
            from models import IncidentAlert, Incident
            from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
            
            incident = Incident.query.get(incident_id)
            hospital = Hospital.query.get(hospital_id)
            
            if not incident or not hospital:
                return False
            
            alert = IncidentAlert(
                incident_id=incident_id,
                hospital_id=hospital_id,
                alert_type=alert_type
            )
            
            message = f"""
            🚨 ACCIDENT ALERT 🚨
            Location: {incident.latitude}, {incident.longitude}
            Type: {incident.incident_type}
            Severity: {incident.severity}
            Status: {incident.status}
            """
            
            if alert_type == 'sms' and TWILIO_ACCOUNT_SID:
                # Send SMS via Twilio (requires proper setup)
                try:
                    from twilio.rest import Client
                    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                    client.messages.create(
                        body=message,
                        from_=TWILIO_PHONE_NUMBER,
                        to=hospital.phone
                    )
                    alert.sent = True
                except:
                    pass
            
            db.session.add(alert)
            db.session.commit()
            return True
        
        except Exception as e:
            print(f"Alert service error: {e}")
            return False
