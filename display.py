from papirus import Papirus
from datetime import datetime
import time
# from keys import weatherApiKey
# import geocoder
from PIL import Image, ImageDraw, ImageFont

DEBUG = True

REGULAR_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

HEADING_SIZE = 35
SUBHEADING_SIZE = 20
REGULAR_SIZE = 17
SMALL_SIZE = 10

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
WEATHER_ICON_BASE_PATH = "./weather_icons/"

SCREEN_WIDTH, SCREEN_HEIGHT = 200, 96

WHITE, BLACK = 1, 0

data = {
  "firstUpdate": True,
  "now": datetime.now(),
  "prevMinute": None,
  "prevHour": None,
  "currentScreenUpdate": None,
  "epd": None,
  "image": None,
  "draw": None,
  "weatherData": {
    "currentWeatherIcon": None,
    "currentWeatherImage": None
  }
}

def init():
  if(DEBUG):
    print("Starting...")

  data["currentScreenUpdate"] = statusUpdate

  data["epd"] = Papirus()
  data["image"] = Image.new('1', data["epd"].size, WHITE)
  data["draw"] = ImageDraw.Draw(data["image"])

def deinit():
  data["epd"].clear()

# Main Loop
def main():
  while(True):
    
    updateScreen(data["prevMinute"] != data["now"].minute or data["firstUpdate"])
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
  if(data["now"].hour == data["prevHour"]):
    data["epd"].partial_update()
  else:
    data["epd"].update()
    
  data["firstUpdate"] = False

# Updates the global values used in the main loop
def updateValues():  
  # Update values
  data["prevMinute"] = data["now"].minute
  data["prevHour"] = data["now"].hour

  # Get current time
  data["now"] = datetime.now()

# Update and draw the status page
def statusUpdate():
  
    # Weather Update
  if(data["now"].minute % 30 == 0 or data["firstUpdate"]):
    if DEBUG:
      print("Weather Data Update")
    
    data["weatherData"]["currentWeatherIcon"] = WEATHER_ICON_BASE_PATH + "icons8-sun-96.png"
    data["weatherData"]["currentWeatherImage"] = Image.open(data["weatherData"]["currentWeatherIcon"]).resize((WEATHER_ICON_SIZE, WEATHER_ICON_SIZE))
  
  # Draw Update
  if(data["prevMinute"] != data["now"].minute or data["firstUpdate"]): 
    if(DEBUG):
      print("Status Update")
    
    # Update the time
    currentTime = data["now"].strftime("%H:%M")
    currentDay = data["now"].strftime("%A")
    currentDate = data["now"].strftime("%b %d")
    
    # Draw the time
    data["draw"].text((SPACING, SPACING), currentTime, fill=BLACK, font=HEADING_FONT)
    data["draw"].text((SPACING, SPACING + HEADING_SIZE + SPACING), currentDay, fill=BLACK, font=REGULAR_FONT)
    data["draw"].text((SPACING, SPACING + HEADING_SIZE + SPACING + REGULAR_SIZE), currentDate, fill=BLACK, font=REGULAR_FONT)

    # Draw the weather
    timeWidth = HEADING_CHAR_WIDTH * len(currentTime)
    weatherIconX = (SCREEN_WIDTH - timeWidth - SPACING - WEATHER_ICON_SIZE)//2 + (SPACING * 2 + timeWidth)
    data["image"].paste(data["weatherData"]["currentWeatherImage"], (weatherIconX, SPACING)) 

if __name__ == "__main__":
  try:
    init()
    main()
  finally:
    if(DEBUG):
      print("Ending...")
    deinit()
