<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>Real-Time Weather Monitoring System</h1>

<p>
    This project is a <strong>Real-Time Weather Monitoring System</strong> built with Flask, SQLAlchemy, and the OpenWeatherMap API.
    It allows users to input a city name to get the current weather, including temperature, feels-like temperature, and weather conditions.
    The system also stores daily summaries and triggers alerts if a user-configured threshold is exceeded.
</p>

<h2>Features</h2>
<ul>
    <li>Fetches and displays weather data for a user-specified city.</li>
    <li>Stores daily summaries in a MySQL database.</li>
    <li>Alerts when the temperature exceeds a specified threshold.</li>
    <li>Refreshes weather data periodically using a background scheduler.</li>
</ul>

<h2>Table of Contents</h2>
<ol>
    <li><a href="#dependencies">Dependencies</a></li>
    <li><a href="#setup-instructions">Setup Instructions</a></li>
    <li><a href="#running-the-application">Running the Application</a></li>
    <li><a href="#api-and-alert-thresholds">API and Alert Thresholds</a></li>
    <li><a href="#design-choices">Design Choices</a></li>
</ol>

<h2 id="dependencies">Dependencies</h2>

<h3>Python Packages</h3>
<p>The following Python packages are required:</p>
<ul>
    <li>Flask</li>
    <li>Flask-SQLAlchemy</li>
    <li>APScheduler</li>
    <li>requests</li>
    <li>PyMySQL</li>
</ul>
<p>Install them with:</p>
<pre><code>pip install flask flask_sqlalchemy apscheduler requests pymysql</code></pre>

<h3>API Key</h3>
<p>Get an API key from <a href="https://home.openweathermap.org/users/sign_up">OpenWeatherMap</a> and replace <code>API_KEY</code> in <code>app.py</code>.</p>

<h2 id="setup-instructions">Setup Instructions</h2>

<ol>
    <li><strong>Clone Repository</strong>
        <pre><code>git clone https://github.com/username/realtime-weather-monitoring-system.git
cd realtime-weather-monitoring-system</code></pre>
    </li>
        <p>This will create a MySQL database named <code>weather_db</code> on <code>localhost:3306</code>.</p>
    <li><strong>Update Configurations in <code>app.py</code></strong>
        <p>In <code>app.py</code>, update the following variables as needed:</p>
        <pre><code>API_KEY = 'your_openweathermap_api_key'
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
REFRESH_TIME = 300  # Refresh interval in seconds
ALERT_THRESHOLD = 20  # Threshold temperature for alerts</code></pre>
    </li>
    <li><strong>Initialize Database Tables</strong>
        <pre><code>python app.py</code></pre>
        <p>This will create the tables defined in <code>app.py</code>.</p>
    </li>
</ol>

<h2 id="running-the-application">Running the Application</h2>

<ol>
    <li><strong>Start the Backend Application</strong>:
        <pre><code>python app.py</code></pre>
    </li>
    <li><strong>Access the Web Interface</strong>:
        <p>Open your browser and go to <a href="http://localhost:5000">http://localhost:5000</a> to access the weather input interface.</p>
    </li>
</ol>

<h2 id="api-and-alert-thresholds">API and Alert Thresholds</h2>

<h3>Weather API</h3>
<p>
    The application uses the <a href="https://openweathermap.org/api">OpenWeatherMap API</a> to retrieve real-time weather data.
    The API response provides temperature, feels-like temperature, and a dominant weather condition.
</p>

<h3>Alerting Thresholds</h3>
<p>Alerts are generated if:</p>
<ul>
    <li>The temperature in a city exceeds a defined threshold (20°C by default). This can be customized in <code>app.py</code>.</li>
</ul>

<h2 id="design-choices">Design Choices</h2>

<ol>
    <li><strong>Flask for Web Server</strong>: Flask provides a lightweight, easy-to-use framework that fits well with smaller projects or microservices like this one.</li>
    <li><strong>SQLAlchemy for ORM</strong>: Flask-SQLAlchemy is used to interact with MySQL. The ORM approach abstracts SQL queries, making data handling simpler and less error-prone.</li>
    <li><strong>APScheduler for Background Jobs</strong>: APScheduler enables periodic fetching of weather data. The <code>BackgroundScheduler</code> is a lightweight option to refresh data without affecting user requests.</li>
    <li><strong>Dockerized MySQL Database</strong>: Using Docker ensures consistency across environments, as users can quickly set up a database with a single command.</li>
</ol>

<h2>Troubleshooting</h2>
<ul>
    <li><strong>MySQL Connection Errors</strong>: Ensure that Docker is running and MySQL is accessible on <code>localhost:3306</code>.</li>
    <li><strong>API Rate Limits</strong>: OpenWeatherMap may limit requests on free API plans. For testing, consider getting an upgraded API plan if hitting rate limits.</li>
</ul>

<h2>License</h2>
<p>This project is open-source, and contributions are welcome.</p>

</body>
</html>
