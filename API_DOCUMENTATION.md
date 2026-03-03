# API Documentation - Accident Hospital Service

## Overview
Complete REST API for accident detection, hospital management, and emergency response.

## Base URL
`http://localhost:5000`

---

## Endpoints

### 1. Location Management

#### Get Current Location
**Endpoint:** `POST /api/location`

**Request:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "accuracy": 25.5
}
```

**Response:**
```json
{
  "success": true,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "accuracy": 25.5,
  "timestamp": "2026-02-26T10:30:45.123456"
}
```

---

### 2. Hospital Search

#### Find Nearest Hospitals
**Endpoint:** `GET /nearest-hospitals` or `POST /nearest-hospitals`

**Query Parameters:**
- `latitude` (float, required) - User latitude
- `longitude` (float, required) - User longitude

**Request Body (POST):**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

**Response:**
```json
{
  "success": true,
  "user_location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "hospitals": [
    {
      "id": 1,
      "name": "City Medical Center",
      "phone": "+1-555-0101",
      "address": "123 Main St, Downtown",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "distance_km": 0.5,
      "ambulance_available": 3,
      "emergency_beds": 8,
      "email": "emergency@citymedical.com"
    }
  ],
  "count": 3
}
```

#### Get All Hospitals
**Endpoint:** `GET /api/hospitals`

**Response:**
```json
{
  "success": true,
  "hospitals": [...],
  "count": 15
}
```

#### Get Specific Hospital
**Endpoint:** `GET /api/hospital/<id>`

**Response:**
```json
{
  "success": true,
  "hospital": {
    "id": 1,
    "name": "City Medical Center",
    ...
  }
}
```

---

### 3. Accident Detection

#### Manual Accident Report
**Endpoint:** `POST /api/report-accident`

**Request:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "description": "Vehicle collision at intersection"
}
```

**Response:**
```json
{
  "success": true,
  "incident_id": 42,
  "message": "Accident reported! 3 hospitals alerted.",
  "hospitals": [
    {
      "name": "City Medical Center",
      "distance_km": 0.5,
      ...
    }
  ]
}
```

#### Sensor-Based Crash Detection
**Endpoint:** `POST /api/sensor-crash-detect`

**Request:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "acceleration": [0.5, 2.3, 75.8],
  "gyroscope": [0.1, 0.2, 250.5]
}
```

**Parameters:**
- `acceleration`: [x, y, z] in m/s²
- `gyroscope`: [alpha, beta, gamma] in °/s

**Response (Crash Detected):**
```json
{
  "crash_detected": true,
  "incident_id": 43,
  "severity": "high",
  "confidence": 85.5,
  "hospitals_alerted": 5,
  "nearest_hospital": {
    "name": "City Medical Center",
    "distance_km": 0.5,
    ...
  }
}
```

**Response (No Crash):**
```json
{
  "crash_detected": false,
  "message": "No crash detected"
}
```

#### Video-Based Crash Detection
**Endpoint:** `POST /api/video-crash-detect`

**Request (multipart/form-data):**
- `video` (file) - Video file from dashboard camera
- `latitude` (float) - Location latitude
- `longitude` (float) - Location longitude

**Response (Crash Detected):**
```json
{
  "video_processed": true,
  "crash_detected": true,
  "confidence": 92.5,
  "video_file": "20260226_153045_crash.mp4",
  "incident_id": 44,
  "hospitals_alerted": 5,
  "nearest_hospital": {
    "name": "City Medical Center",
    ...
  }
}
```

**Response (No Crash):**
```json
{
  "video_processed": true,
  "crash_detected": false,
  "confidence": 15.3,
  "video_file": "20260226_153045_video.mp4"
}
```

---

### 4. Incident Management

#### Get All Incidents
**Endpoint:** `GET /api/incidents`

**Response:**
```json
{
  "success": true,
  "incidents": [
    {
      "id": 42,
      "user_id": "user123",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "incident_type": "manual_report",
      "severity": "high",
      "confidence": null,
      "status": "reported",
      "created_at": "2026-02-26T10:30:45.123456",
      "hospital_id": 1
    }
  ],
  "count": 15
}
```

#### Get Specific Incident
**Endpoint:** `GET /api/incident/<id>`

**Response:**
```json
{
  "success": true,
  "incident": {
    "id": 42,
    "user_id": "user123",
    ...
  }
}
```

#### Update Incident Status
**Endpoint:** `PUT /api/incident/<id>`

**Request:**
```json
{
  "status": "dispatched",
  "hospital_id": 1,
  "notes": "Ambulance dispatched to scene"
}
```

**Response:**
```json
{
  "success": true,
  "incident": {
    "id": 42,
    "status": "dispatched",
    ...
  }
}
```

---

### 5. File Serving

#### Download Uploaded Video
**Endpoint:** `GET /uploads/<filename>`

**Response:** Video file stream

---

### 6. System Health

#### Health Check
**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "Accident Hospital Service",
  "version": "1.0.0",
  "timestamp": "2026-02-26T10:30:45.123456"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Latitude and longitude required"
}
```

### 404 Not Found
```json
{
  "error": "Incident not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error message"
}
```

---

## Request Headers

```
Content-Type: application/json
Accept: application/json
```

For file uploads:
```
Content-Type: multipart/form-data
```

---

## Incident Types

- `manual_report` - User manually reported
- `crash` - Detected via sensor data
- `ai_detection` - Detected via video analysis

## Severity Levels

- `low` - Minor incident
- `medium` - Moderate incident
- `high` - Serious incident
- `critical` - Life-threatening

## Incident Status

- `reported` - Initial report received
- `dispatched` - Ambulance dispatched
- `arrived` - Ambulance arrived at scene
- `resolved` - Incident handled

---

## Rate Limiting

Currently no rate limiting. For production:
- Location updates: 10 requests/minute
- Detection requests: 5 requests/minute
- Hospital search: Unlimited

---

## Authentication

Currently no authentication required. For production, implement:
- API keys for external access
- JWT tokens for web frontend
- OAuth2 for mobile apps

---

## CORS

CORS is enabled for all origins. For production, restrict to:
```python
CORS(app, resources={
    r"/api/*": {"origins": ["https://yourdomain.com"]}
})
```

---

## Data Validation

- Latitude: -90 to 90
- Longitude: -180 to 180
- Acceleration: -500 to 500 m/s²
- Gyroscope: -360 to 360 °/s
- File size: Max 50MB

---

## Example Usage

### JavaScript/Fetch

```javascript
// Report accident
fetch('/api/report-accident', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    latitude: 40.7128,
    longitude: -74.0060,
    description: 'Car collision'
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

### Python/Requests

```python
import requests

# Find nearby hospitals
response = requests.get(
    'http://localhost:5000/nearest-hospitals',
    params={
        'latitude': 40.7128,
        'longitude': -74.0060
    }
)
hospitals = response.json()
print(hospitals)
```

### cURL

```bash
# Manual accident report
curl -X POST http://localhost:5000/api/report-accident \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 40.7128,
    "longitude": -74.0060,
    "description": "Vehicle collision"
  }'

# Video upload
curl -X POST http://localhost:5000/api/video-crash-detect \
  -F "video=@video.mp4" \
  -F "latitude=40.7128" \
  -F "longitude=-74.0060"
```

---

## WebSocket (Future Enhancement)

Real-time updates via WebSocket:
```
ws://localhost:5000/ws/incidents
```

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-26
