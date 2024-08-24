import requests
import sys

def fetch_weather(zip_code, country_code, api_key):
    # OpenWeatherMap API URL
    url = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        # Parse the JSON response
        weather_data = response.json()

        # Extract data
        location = weather_data['name']
        temperature = weather_data['main']['temp']
        temperature_feel = weather_data['main']['feels_like']
        weather_description = weather_data['weather'][0]['main']


        return {
            'location': location,
            'temperature': temperature,
            'description': weather_description,
            'feels like' : temperature_feel
        }

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"

def main():
    # Replace 'your_api_key_here' with your actual OpenWeatherMap API key
    api_key = '27aabfd1b75f4ea533d19c7351c4284c' 

    while True:
        zip_code = input("Enter the zip/postal code: ")
        country_code = input("Enter the country code (e.g., US for United States, GB for United Kingdom): ")
        weather = fetch_weather(zip_code, country_code, api_key)
            
            
        
        if isinstance(weather, dict):
            print(f"Location: {weather['location']}")
            print(f"Temperature: {weather['temperature']}°C")
            print(f"Feels Like: {weather['feels like']}°C")
            print(f"Weather: {weather['description']}")
            sys.exit() # closes program after user is provided with weather
        else:
            print("Invalid Input")
            continue 
        #Loops to ask the user for input again if invalid input is given

if __name__ == "__main__":
    main()