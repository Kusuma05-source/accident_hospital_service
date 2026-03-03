# Quick Start Guide - 5 Minutes to Running

## Step 1: Start the Application (30 seconds)

### Windows:
```bash
# Double-click:
run.bat
```

### Mac/Linux:
```bash
chmod +x run.sh
./run.sh
```

### Manual (Any OS):
```bash
# Activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run app
python app.py
```

**Your app is now running at: `http://localhost:5000`**

---

## Step 2: Configure API Keys (2 minutes)

### Google Maps API (Recommended)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable "Maps Places API"
4. Create API key
5. Edit `.env` file:
   ```
   GOOGLE_MAPS_API_KEY=paste_your_key_here
   ```

### Twilio SMS Alerts (Optional)
1. Sign up at [Twilio.com](https://www.twilio.com)
2. Get Account SID and Auth Token
3. Buy a phone number
4. Edit `.env`:
   ```
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_PHONE_NUMBER=+1234567890
   ```

---

## Step 3: Test the Features (3 minutes)

### Test Location Tracking:
1. Open browser: `http://localhost:5000`
2. Click **Location** tab
3. Click **"Get My Location"**
4. Allow location permission
5. See your coordinates displayed

### Test Hospital Search:
1. Click **Hospitals** tab
2. Click **"Find Nearby Hospitals"**
3. See hospitals within 5km radius with distances

### Test Manual Report:
1. Click **Detection** tab
2. Enter accident description
3. Click **"Report Accident"**
4. See confirmation and nearby hospitals

### Test Sensor Monitoring:
1. Click **Detection** tab
2. Click **"Start Sensor Monitoring"**
3. Move your device
4. Watch accelerometer and gyroscope values update

### Test Video Analysis:
1. Click **Detection** tab
2. Upload any video file
3. Click **"Analyze Video"**
4. See analysis results

---

## Features Overview

### 📍 Location Tab
- Display current latitude/longitude
- GPS accuracy information
- Start continuous tracking
- Track every 5 seconds

### 🚨 Detection Tab
- **Manual Report**: Report accidents manually
- **Sensor Detection**: Crash detection via phone accelerometer
- **Video Analysis**: Analyze dashboard/phone camera video

### 🏥 Hospitals Tab
- Find nearby hospitals
- Distance calculation
- Ambulance availability
- Emergency beds available

### 📋 Incidents Tab
- View all reported incidents
- Incident details and status
- Severity information
- Timestamp of reports

### 📊 Status Tab
- System health check
- Total incidents count
- Available hospitals
- API status

---

## First Time Setup Checklist

- [ ] Install Python 3.8+
- [ ] Clone/download project
- [ ] Run `pip install -r requirements.txt`
- [ ] Edit `.env` file with your API keys
- [ ] Run `python app.py`
- [ ] Open `http://localhost:5000`
- [ ] Enable browser location permission
- [ ] Test location feature
- [ ] Test hospital search

---

## Common Issues & Solutions

### ❌ "Port 5000 already in use"
```bash
# Change port in .env:
PORT=5001

# Then restart app
```

### ❌ "Location permission denied"
- Click browser settings
- Allow location access for localhost
- Try incognito mode (sometimes helps)

### ❌ "No hospitals found"
- Check `.env` has valid Google Maps API key
- Or system uses sample hospitals (always available)
- Check internet connection

### ❌ "Video analysis too slow"
- Use smaller video file
- Reduce resolution
- Check system resources

### ❌ "Sensors not working on iOS"
- Requires iOS 13+
- Must enable DeviceMotionEvent permission
- Try Chrome app instead of Safari

---

## Next Steps

### 1. Get Google Maps API Key
- Takes 5 minutes
- Free tier: $200/month credit
- [Get API Key](https://console.cloud.google.com/)

### 2. Setup Hospital Database
- Edit `models.py` to add more hospitals
- Or use Google Maps API for real data
- Or import hospital database via CSV

### 3. Deploy to Cloud
- Heroku (free tier available)
- AWS (with bill)
- Google Cloud
- Digital Ocean

### 4. Mobile App Integration
- Use same API endpoints
- iOS app with Swift
- Android app with Kotlin
- React Native for both

---

## Testing with cURL

### Test Location Endpoint:
```bash
curl -X POST http://localhost:5000/api/location \
  -H "Content-Type: application/json" \
  -d '{"latitude":40.7128,"longitude":-74.0060,"accuracy":25}'
```

### Test Hospital Search:
```bash
curl http://localhost:5000/nearest-hospitals \
  -d "latitude=40.7128&longitude=-74.0060"
```

### Test Sensor Detection:
```bash
curl -X POST http://localhost:5000/api/sensor-crash-detect \
  -H "Content-Type: application/json" \
  -d '{
    "latitude":40.7128,
    "longitude":-74.0060,
    "acceleration":[0.5,2.3,75.8],
    "gyroscope":[0.1,0.2,250.5]
  }'
```

### Test Accident Report:
```bash
curl -X POST http://localhost:5000/api/report-accident \
  -H "Content-Type: application/json" \
  -d '{
    "latitude":40.7128,
    "longitude":-74.0060,
    "description":"Vehicle collision at intersection"
  }'
```

### Health Check:
```bash
curl http://localhost:5000/api/health
```

---

## Database Reset

To reset database (delete all incidents):
```bash
# Delete database file
rm accident_service.db  # Linux/Mac
del accident_service.db # Windows

# Restart app - it will create fresh database
python app.py
```

---

## Performance Tips

1. **Location Tracking**: Disable when not needed
2. **Sensor Monitoring**: High CPU usage, disable when not monitoring
3. **Video Analysis**: Can take 10-30 seconds, run in background
4. **Hospital Search**: Results cached, reuse if location not changed
5. **Database**: Use SQLite for development, PostgreSQL for production

---

## Deployment Checklist

Before going live:
- [ ] Replace default secret key in `.env`
- [ ] Use strong API keys
- [ ] Enable HTTPS
- [ ] Add authentication
- [ ] Setup proper logging
- [ ] Configure real hospital database
- [ ] Test with real emergency contacts
- [ ] Setup SMS service (Twilio)
- [ ] Add rate limiting
- [ ] Backup database regularly

---

## Getting Help

1. **Check README.md** for full documentation
2. **Read API_DOCUMENTATION.md** for API details
3. **Check browser console** (F12) for errors
4. **Check server logs** in terminal
5. **Enable debug mode** in `.env`: `DEBUG=True`

---

## Next Advanced Steps

- [ ] Add machine learning crash detection
- [ ] Real-time WebSocket updates
- [ ] Mobile push notifications
- [ ] Police/Fire department integration
- [ ] Insurance provider integration
- [ ] Traffic analysis
- [ ] Emergency service routing
- [ ] Multi-language support

---

**You're all set! 🚀 Start at http://localhost:5000**

Enjoy building your emergency response system!
