# wsgi.py
"""
from flask import Flask

# Create the Flask app instance
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"
"""
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your OpenWeatherMap API Key
API_KEY = '50b1f5d6fa54fd8e9ea405268da42022'

# Base URL for the weather API
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get('city')

        if city:
            try:
                # API request to get weather data
                response = requests.get(BASE_URL, params={
                    'q': city,
                    'appid': API_KEY,
                    'units': 'metric'  # Get temperature in Celsius
                })
                data = response.json()

                if response.status_code == 200:
                    weather_data = {
                        'city': data['name'],
                        'temperature': data['main']['temp'],
                        'humidity': data['main']['humidity'],
                        'condition': data['weather'][0]['description'],
                        'icon': data['weather'][0]['icon']
                    }
                else:
                    error = "City not found. Please try again."

            except Exception as e:
                error = f"Error occurred: {str(e)}"

    return render_template("index.html", weather_data=weather_data, error=error)


if __name__ == "__main__":
    app.run(debug=True)
