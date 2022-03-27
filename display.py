#!/usr/bin/env python3
from papirus import Papirus, PapirusComposite, LM75B
from datetime import datetime
import time
from keys import weatherApiKey
import geocoder
from PIL import Image, ImageDraw, ImageFont
from enum import Enum

class IDS(Enum):
  TIME = "Time"
  DAY = "Day"
  DATE = "Date"
  WEATHER_ICON = "WeatherIcon"

TEXT_SIZE = 35
SUBTEXT_SIZE = 17

REGULAR_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

WEATHER_ICON_SIZE = 25
WEATHER_ICON_X = 120
WEATHER_ICON_Y = 5

# REGULAR_FONT = ImageFont.truetype(REGULAR_FONT_PATH, TEXT_SIZE)
# REGULAR_CHAR_WIDTH = REGULAR_FONT.getsize("0")[0]
# BOLD_FONT = ImageFont.truetype(BOLD_FONT_PATH, SUBTEXT_SIZE)
# BOLD_CHAR_WIDTH = BOLD_FONT.getsize("0")[0]

WHITE, BLACK = 1, 0

WEATHER_ICON_BASE = "./weather_icons/"

updateFrame = False
firstUpdate = True

prevMinute = -1
now = datetime.now()

currentWeatherIcon = "icons8-sun-96"

def init():
  global composite, screen, image, draw, sensor
  
  print("Starting...")

  composite = PapirusComposite(False)
  composite.partialUpdates = True
  screen = Papirus()
  composite.partialUpdates = True
  image = Image.new('1', screen.size, WHITE)
  draw = ImageDraw.Draw(image)
  
  # TODO Move this to the screen switching code
  initStatus()
  
def deinit():
  composite.Clear()
  
def main():
  global now, prevMinute, updateFrame, firstUpdate
  
  while(True):
    # Get current time
    now = datetime.now()
    
    # Update the screen
    statusUpdate()
    
    # Update values
    prevMinute = now.minute
    
    if updateFrame:
      print("Main Update")
      composite.WriteAll()
      updateFrame = False
    
    firstUpdate = False
    
    # Sleep
    time.sleep(1)
    
def initStatus():
  global updateFrame
  
  print("Status Init")
  composite.AddText(text=now.strftime("%H:%M"), x=5, y=5, size=TEXT_SIZE, Id=IDS.TIME.value, fontPath=BOLD_FONT_PATH)
  composite.AddText(text=now.strftime("%A"), x=5, y=TEXT_SIZE + 15, size=SUBTEXT_SIZE, Id=IDS.DAY.value, fontPath=REGULAR_FONT_PATH)
  composite.AddText(text=now.strftime("%b %d"), x=5, y=TEXT_SIZE + 15 + SUBTEXT_SIZE, size=SUBTEXT_SIZE, Id=IDS.DATE.value, fontPath=REGULAR_FONT_PATH)
  
  composite.AddImg(WEATHER_ICON_BASE + currentWeatherIcon, WEATHER_ICON_X, WEATHER_ICON_Y, (WEATHER_ICON_SIZE, WEATHER_ICON_SIZE), Id=IDS.WEATHER_ICON.value)

def statusUpdate():
  global updateFrame, composite
  
  # Time Update
  if(prevMinute != now.minute or firstUpdate): 
    print("Status Update")
    updateFrame = True
    
    currentTime = now.strftime("%H:%M")
    currentDay = now.strftime("%A")
    currentDate = now.strftime("%b %d")
    
    composite.UpdateText(IDS.TIME.value, currentTime, BOLD_FONT_PATH)
    composite.UpdateText(IDS.DAY.value, currentDay, REGULAR_FONT_PATH)
    composite.UpdateText(IDS.DATE.value, currentDate, REGULAR_FONT_PATH)
  
  # Weather Update
  if(now.minute % 1 == 0 or firstUpdate):
    composite.UpdateImg(IDS.WEATHER_ICON.value, WEATHER_ICON_BASE + currentWeatherIcon)

if __name__ == "__main__":
  try:
    init()
    main()
  finally:
    print("Ending...")
    deinit()
