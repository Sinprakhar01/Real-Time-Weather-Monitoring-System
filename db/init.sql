Create database weather_db;

CREATE TABLE daily_weather_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50),
    date DATE,
    avg_temp DECIMAL(5, 2),
    max_temp DECIMAL(5, 2),
    min_temp DECIMAL(5, 2),
    dominant_weather VARCHAR(50),
    feels_like DECIMAL(5,2)
)

CREATE TABLE alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50),
    message VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);