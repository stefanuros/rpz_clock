from papirus import Papirus
from datetime import datetime
import time
from keys import weatherApiKey
import geocoder
from PIL import Image, ImageDraw, ImageFont
import threading
import requests

DEBUG = False

REGULAR_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

HEADING_SIZE = 35
SUBHEADING_SIZE = 20
REGULAR_SIZE = 15
SMALL_SIZE = 12

HEADING_FONT = ImageFont.truetype(BOLD_FONT_PATH, HEADING_SIZE)
HEADING_CHAR_WIDTH = HEADING_FONT.getsize("0")[0]
SUBHEADING_FONT = ImageFont.truetype(REGULAR_FONT_PATH, SUBHEADING_SIZE)
SUBHEADING_CHAR_WIDTH = SUBHEADING_FONT.getsize("0")[0]
REGULAR_FONT = ImageFont.truetype(REGULAR_FONT_PATH, REGULAR_SIZE)
REGULAR_CHAR_WIDTH = REGULAR_FONT.getsize("0")[0]
SMALL_FONT = ImageFont.truetype(REGULAR_FONT_PATH, SMALL_SIZE)
SMALL_CHAR_WIDTH = SMALL_FONT.getsize("0")[0]

SPACING = 5

WEATHER_ICON_SIZE = 48
WEATHER_ICON_BASE_PATH = "/home/pi/projects/rpz_status/weather_icons/"

SCREEN_WIDTH, SCREEN_HEIGHT = 200, 96

WHITE, BLACK = 1, 0

WEATHER_ICON= {
  "01d": "icons8-sun-90.png",
  "01n": "icons8-sun-90.png",
  "02d": "icons8-partly-cloudy-day-90.png",
  "02n": "icons8-partly-cloudy-day-90.png",
  "03d": "icons8-partly-cloudy-day-90.png",
  "03n": "icons8-partly-cloudy-day-90.png",
  "04d": "icons8-clouds-90.png",
  "04n": "icons8-clouds-90.png",
  "09d": "icons8-rain-90.png",
  "09n": "icons8-rain-90.png",
  "10d": "icons8-rain-cloud-90.png",
  "10n": "icons8-rain-cloud-90.png",
  "11d": "icons8-storm-90.png",
  "11n": "icons8-storm-90.png",
  "13d": "icons8-snow-90.png",
  "13n": "icons8-snow-90.png",
  "50d": "icons8-haze-90.png",
  "50n": "icons8-haze-90.png",
  "UNKNOWN": "icons8-query-90.png"
}

data = {
  "firstUpdate": True,
  "now": datetime.now(),
  "prevMinute": -1,
  "prevHour": -1,
  "currentScreenUpdate": None,
  "epd": None,
  "image": None,
  "draw": None,
  "weatherData": {
    "currentWeatherIcon": WEATHER_ICON_BASE_PATH + WEATHER_ICON["01d"],
    "currentWeatherImage": Image.open(WEATHER_ICON_BASE_PATH + WEATHER_ICON["01d"]).resize((WEATHER_ICON_SIZE, WEATHER_ICON_SIZE)),
    "retryWeather": False,
    "data": {
      "main": {
        "temp": 0,
        "feels_like": 0,
        "temp_min": 0,
        "temp_max": 0
      }
    }
  }
}

def init():
  if(DEBUG):
    print("Starting...")

  data["currentScreenUpdate"] = statusUpdate

  data["epd"] = Papirus()
  data["image"] = Image.new('1', data["epd"].size, WHITE)
  data["draw"] = ImageDraw.Draw(data["image"])
  
  data["epd"].clear()

def deinit():
  data["epd"].clear()

# Main Loop
def main():
  while(True):
    
    updateScreen(
      data["prevMinute"] != data["now"].minute 
      or data["firstUpdate"]
    )
    updateValues()

    # Sleep
    time.sleep(1)

# Contains the update logic to push changes to the screen. Does not draw to screen
def updateScreen(shouldUpdate):
  if not shouldUpdate:
    return
    
  if(DEBUG):
    print("Main Update")

  # Clear the screen
  data["draw"].rectangle([(0,0), (SCREEN_WIDTH, SCREEN_HEIGHT)], fill=WHITE, outline=WHITE)

  # Update the screen
  data["currentScreenUpdate"]()

  data["epd"].display(data["image"])
  
  if(data["now"].hour != data["prevHour"]):
    data["epd"].clear()
    
  if(data["now"].minute % 10 == 0 or data["firstUpdate"]):
    data["epd"].update()
  else:
    data["epd"].partial_update()
    
  data["firstUpdate"] = False

# Updates the global values used in the main loop
def updateValues():  
  # Update values
  data["prevMinute"] = data["now"].minute
  data["prevHour"] = data["now"].hour

  # Get current time
  data["now"] = datetime.now()

def fetchWeatherData():
  if DEBUG:
    print("Getting weather data")
    
  lat, long = geocoder.ip('me').latlng
  
  params = {
    "lat": str(lat),
    "lon": str(long),
    "appid": weatherApiKey,
    "units": "metric"  
  }
  
  response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
  
  if(not response.ok):
    data["retryWeather"] = True
    print("Get weather failed for the following reason")
    print(str(response.status_code) + ": " + response.reason)
    return
  
  json = response.json()
  
  data["weatherData"]["data"] = json
  
  if json["weather"][0]["icon"] in WEATHER_ICON:
    data["weatherData"]["currentWeatherIcon"] = WEATHER_ICON_BASE_PATH + WEATHER_ICON[json["weather"][0]["icon"]]
  else:
    data["weatherData"]["currentWeatherIcon"] = WEATHER_ICON_BASE_PATH + WEATHER_ICON["UNKNOWN"]
  data["weatherData"]["currentWeatherImage"] = Image.open(data["weatherData"]["currentWeatherIcon"]).resize((WEATHER_ICON_SIZE, WEATHER_ICON_SIZE))
  
  if DEBUG:
    print("Finished Weather fetching")

# Update and draw the status page
def statusUpdate():
  isNextMinute = data["prevMinute"] != data["now"].minute
  
  # Weather Update
  if(
    (data["now"].minute % 10 == 0 and isNextMinute)
    or data["firstUpdate"] 
    or (data["weatherData"]["retryWeather"] and isNextMinute)
  ):
    weatherFetcher = threading.Thread(target=fetchWeatherData)
    weatherFetcher.start()
    if(data["firstUpdate"]):
      weatherFetcher.join()
  
  # Draw Update
  if(isNextMinute or data["firstUpdate"]): 
    if(DEBUG):
      print("Status Update")
    
    # Update the time
    currentTime = data["now"].strftime("%H:%M")
    currentDay = data["now"].strftime("%A")
    currentDate = data["now"].strftime("%b %d")
    
    # Draw the time
    data["draw"].text((SPACING, SPACING), currentTime, fill=BLACK, font=HEADING_FONT)
    data["draw"].text((SPACING, (2*SPACING) + HEADING_SIZE), currentDay, fill=BLACK, font=SUBHEADING_FONT)
    data["draw"].text((SPACING, (3*SPACING) + HEADING_SIZE + REGULAR_SIZE), currentDate, fill=BLACK, font=SUBHEADING_FONT)

    # Draw the weather
    timeWidth = (HEADING_CHAR_WIDTH * len(currentTime)) + SPACING
    weatherX = round((SCREEN_WIDTH - timeWidth - WEATHER_ICON_SIZE)/2 + timeWidth)
    data["image"].paste(data["weatherData"]["currentWeatherImage"], (weatherX, SPACING)) 
    
    temp = round(data["weatherData"]["data"]["main"]["temp"])
    tempText = f"{temp}\u00b0C"
    tempWidth = len(tempText) * SUBHEADING_CHAR_WIDTH
    
    feelsLike = round(data["weatherData"]["data"]["main"]["feels_like"])
    if(feelsLike == temp):
      feelsLikeText = ""
    else:
      feelsLikeText = f"{feelsLike}\u00b0C"
    feelsLikeWidth = len(feelsLikeText) * SMALL_CHAR_WIDTH
    
    tempX = (SCREEN_WIDTH - timeWidth - (tempWidth + feelsLikeWidth))/2 + timeWidth
    feelsLikeX = tempX + tempWidth
    
    highTemp = round(data["weatherData"]["data"]["main"]["temp_max"])
    lowTemp = round(data["weatherData"]["data"]["main"]["temp_min"])
    highLowText = f"{lowTemp}\u00b0C/{highTemp}\u00b0C"
    highLowWidth = len(highLowText) * REGULAR_CHAR_WIDTH
    highLowX = (SCREEN_WIDTH - timeWidth - highLowWidth)/2 + timeWidth
    
    data["draw"].text((tempX, SPACING + WEATHER_ICON_SIZE), tempText, fill=BLACK, font=SUBHEADING_FONT)
    data["draw"].text((feelsLikeX, SPACING + WEATHER_ICON_SIZE + (SUBHEADING_SIZE - SMALL_SIZE)), feelsLikeText, fill=BLACK, font=SMALL_FONT)
    data["draw"].text((highLowX, SPACING + WEATHER_ICON_SIZE + SUBHEADING_SIZE + 2), highLowText, fill=BLACK, font=REGULAR_FONT)

if __name__ == "__main__":
  try:
    print("Starting...")
    init()
    main()
  finally:
    print("Ending...")
    deinit()
