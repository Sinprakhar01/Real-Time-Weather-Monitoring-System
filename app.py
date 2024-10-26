from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# config
API_KEY = '14a91cf73454cf0e08aa8d5688c206ea'
REFRESH_TIME=5 #In minutes
ALERT_THRESHOLD=20 
DB_USERNAME='root'
DB_PASSWORD='root'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/weather_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for Daily Weather Summary
class DailyWeatherSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    avg_temp = db.Column(db.Float, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)
    min_temp = db.Column(db.Float, nullable=False)
    dominant_weather = db.Column(db.String(100), nullable=False)
    feels_like= db.Column(db.Float)

# Database model for Alerts
class Alerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"] - 273.15  # Convert from Kelvin to Celsius
        feels_like = data["main"]["feels_like"] - 273.15  # Convert feels_like from Kelvin to Celsius
        weather_condition = data["weather"][0]["main"]
        
        return {
            "city": city,
            "temperature": round(temperature, 2),
            "feels_like": round(feels_like, 2),
            "weather_condition": weather_condition,
            "date": datetime.now().date()
        }
    else:
        return None
    
def refresh_weather_data():
    with app.app_context():
        weather_stored_data=DailyWeatherSummary.query.all()
        for weather in weather_stored_data:
            weather_data=fetch_weather_data(weather.city)
            print(weather_data)
            store_daily_summary(weather_data)
   
        
def store_daily_summary(weather_data):
    date = weather_data['date']
    city = weather_data['city']
    
    # Check for existing summaries for the current day
    existing_summary = DailyWeatherSummary.query.filter_by(city=city, date=date).first()

    if existing_summary:
        # Update existing summary
        existing_summary.max_temp = max(existing_summary.max_temp, weather_data['temperature'])
        existing_summary.min_temp = min(existing_summary.min_temp, weather_data['temperature'])
        existing_summary.avg_temp = (existing_summary.avg_temp + weather_data['temperature']) / 2
    else:
        # Create a new summary
        new_summary = DailyWeatherSummary(
            city=city,
            date=date,
            avg_temp=weather_data['temperature'],
            max_temp=weather_data['temperature'],
            min_temp=weather_data['temperature'],
            dominant_weather=weather_data['weather_condition'],
            feels_like=weather_data['feels_like']
        )
        db.session.add(new_summary)

    db.session.commit()

def check_alerts(weather_data, thresholds):
    city = weather_data['city']
    temperature = weather_data['temperature']
    
    if temperature > thresholds['temperature']:
        alert_message = f"Temperature in {city} has exceeded {thresholds['temperature']}°C"
        alert = Alerts(city=city, message=alert_message)
        db.session.add(alert)
        db.session.commit()
        return alert_message
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = fetch_weather_data(city)

    if weather_data:
        store_daily_summary(weather_data)
        thresholds = {'temperature': ALERT_THRESHOLD}  # Example threshold
        alert_message = check_alerts(weather_data, thresholds)

        response_data = {
            "weather_data": weather_data,
             "alert": alert_message
        }
        return jsonify(response_data)
    else:
        return jsonify({"error": "City not found or API limit reached."}), 404

@app.route('/alerts')
def get_alerts():
    alerts = Alerts.query.all()
    data = [
        {
            "city": alert.city,
            "message": alert.message,  # Changed from alert_type and alert_value to message
            "timestamp": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for alert in alerts
    ]
    return jsonify(data)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: refresh_weather_data(), 'interval', seconds=REFRESH_TIME)
    scheduler.start()

with app.app_context():
    db.create_all()
if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True)