from papirus import Papirus, PapirusComposite
from datetime import datetime
import time
# from keys import weatherApiKey
# import geocoder
# from PIL import Image, ImageDraw, ImageFont
from enum import Enum

class IDS(Enum):
  TIME = "Time"
  DAY = "Day"
  DATE = "Date"
  WEATHER_ICON = "WeatherIcon"
  TEMP = "Temp"
  TEMP_RANGE = "TempRange"

TEXT_SIZE = 35
SUBTEXT_SIZE = 17

REGULAR_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

WEATHER_ICON_SIZE = 50
WEATHER_ICON_BASE = "./weather_icons/"

DEBUG = True

# REGULAR_FONT = ImageFont.truetype(REGULAR_FONT_PATH, TEXT_SIZE)
# REGULAR_CHAR_WIDTH = REGULAR_FONT.getsize("0")[0]
# BOLD_FONT = ImageFont.truetype(BOLD_FONT_PATH, SUBTEXT_SIZE)
# BOLD_CHAR_WIDTH = BOLD_FONT.getsize("0")[0]

# WHITE, BLACK = 1, 0

firstUpdate = True

prevMinute = -1
prevHour = -1
now = datetime.now()

currentWeatherIcon = "icons8-sun-48.png"

def init():
  global composite
  
  if(DEBUG):
    print("Starting...")

  composite = PapirusComposite(False)
  
  # TODO Move this to the screen switching code
  initStatus()
  
def deinit():
  composite.Clear()
  
def main():
  global now, prevMinute, prevHour, firstUpdate
  
  while(True):
    # Get current time
    now = datetime.now()
    
    # Update the screen
    statusUpdate()
    
    if prevMinute != now.minute or firstUpdate:
      if(DEBUG):
        print("Main Update")
      updateFrame = False
      firstUpdate = False
      
      composite.WriteAll(now.hour == prevHour)

    # Update values
    prevMinute = now.minute
    prevHour = now.hour
      
    # Sleep
    time.sleep(1)
    
def initStatus():  
  if(DEBUG):
    print("Status Init")
  composite.AddText(text="", x=5, y=5, size=TEXT_SIZE, Id=IDS.TIME.value, fontPath=BOLD_FONT_PATH)
  composite.AddText(text="", x=5, y=TEXT_SIZE + 15, size=SUBTEXT_SIZE, Id=IDS.DAY.value, fontPath=REGULAR_FONT_PATH)
  composite.AddText(text="", x=5, y=TEXT_SIZE + 15 + SUBTEXT_SIZE, size=SUBTEXT_SIZE, Id=IDS.DATE.value, fontPath=REGULAR_FONT_PATH)
  
  composite.AddImg(WEATHER_ICON_BASE + currentWeatherIcon, 130, 5, (WEATHER_ICON_SIZE, WEATHER_ICON_SIZE), Id=IDS.WEATHER_ICON.value)
  composite.AddText(text="", x=130, y=WEATHER_ICON_SIZE + 10, size=20, Id=IDS.TEMP.value, fontPath=REGULAR_FONT_PATH)
  composite.AddText(text="", x=110, y=WEATHER_ICON_SIZE + 30, size=10, Id=IDS.TEMP_RANGE.value, fontPath=REGULAR_FONT_PATH)

def statusUpdate():
  global composite
  
  # Time Update
  if(prevMinute != now.minute or firstUpdate): 
    if(DEBUG):
      print("Status Update")
    
    currentTime = now.strftime("%H:%M")
    currentDay = now.strftime("%A")
    currentDate = now.strftime("%b %d")
    
    composite.UpdateText(IDS.TIME.value, currentTime, BOLD_FONT_PATH)
    composite.UpdateText(IDS.DAY.value, currentDay, REGULAR_FONT_PATH)
    composite.UpdateText(IDS.DATE.value, currentDate, REGULAR_FONT_PATH)
  
  # Weather Update
  if(now.minute % 30 == 0 or firstUpdate):
    composite.UpdateImg(IDS.WEATHER_ICON.value, WEATHER_ICON_BASE + currentWeatherIcon)
    composite.UpdateText(IDS.TEMP.value, "21\u00b0C", REGULAR_FONT_PATH)
    composite.UpdateText(IDS.TEMP_RANGE.value, "17\u00b0C/21\u00b0C", REGULAR_FONT_PATH)

if __name__ == "__main__":
  try:
    init()
    main()
  finally:
    if(DEBUG):
      print("Ending...")
    deinit()
