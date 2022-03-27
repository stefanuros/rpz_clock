from papirus import Papirus, PapirusComposite
from datetime import datetime
import time
# from keys import weatherApiKey
# import geocoder
from PIL import Image, ImageDraw, ImageFont
from enum import Enum

DEBUG = True

class IDS(Enum):
  TIME = "Time"
  DAY = "Day"
  DATE = "Date"
  WEATHER_ICON = "WeatherIcon"
  TEMP = "Temp"
  TEMP_RANGE = "TempRange"

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

WEATHER_ICON_SIZE = 50
WEATHER_ICON_BASE = "./weather_icons/"

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 96

WHITE, BLACK = 1, 0

firstUpdate = True

prevMinute = -1
prevHour = -1
now = datetime.now()

currentWeatherIcon = "icons8-sun-48.png"

def init():
  global epd, image, draw
  
  if(DEBUG):
    print("Starting...")

  # composite = PapirusComposite(False)
  
  epd = Papirus()
  image = Image.new('1', epd.size, WHITE)
  draw = ImageDraw.Draw(image)
  
  # TODO Move this to the screen switching code
  initStatus()
  
def deinit():
  epd.clear()
  # composite.Clear()
  
def main():
  global now, prevMinute, prevHour, firstUpdate
  
  while(True):
    # Get current time
    now = datetime.now()
    
    # Clear the screen
    draw.rectangle([(0,0), (SCREEN_WIDTH, SCREEN_HEIGHT)], fill=WHITE, outline=WHITE)
    
    # Update the screen
    statusUpdate()
    
    if prevMinute != now.minute or firstUpdate:
      if(DEBUG):
        print("Main Update")
      firstUpdate = False
      
      # Do a full update every hour
      # composite.WriteAll(now.hour == prevHour)
      
      epd.display(image)
      if(now.hour == prevHour):
        epd.partial_update()
      else:
        epd.update()

    # Update values
    prevMinute = now.minute
    prevHour = now.hour
      
    # Sleep
    time.sleep(1)
    
def initStatus():  
  if(DEBUG):
    print("Status Init")
  # composite.AddText(text="", x=SPACING, y=SPACING, size=HEADING_SIZE, Id=IDS.TIME.value, fontPath=BOLD_FONT_PATH)
  # composite.AddText(text="", x=SPACING, y=HEADING_SIZE + 15, size=REGULAR_SIZE, Id=IDS.DAY.value, fontPath=REGULAR_FONT_PATH)
  # composite.AddText(text="", x=SPACING, y=HEADING_SIZE + 15 + REGULAR_SIZE, size=REGULAR_SIZE, Id=IDS.DATE.value, fontPath=REGULAR_FONT_PATH)
  
  # composite.AddImg(WEATHER_ICON_BASE + currentWeatherIcon, 130, SPACING, (WEATHER_ICON_SIZE, WEATHER_ICON_SIZE), Id=IDS.WEATHER_ICON.value)
  # composite.AddText(text="", x=130, y=WEATHER_ICON_SIZE + 10, size=SUBHEADING_SIZE, Id=IDS.TEMP.value, fontPath=REGULAR_FONT_PATH)
  # composite.AddText(text="", x=130, y=WEATHER_ICON_SIZE + 30, size=SMALL_SIZE, Id=IDS.TEMP_RANGE.value, fontPath=REGULAR_FONT_PATH)

def statusUpdate():
  # Time Update
  if(prevMinute != now.minute or firstUpdate): 
    if(DEBUG):
      print("Status Update")
    
    currentTime = now.strftime("%H:%M")
    currentDay = now.strftime("%A")
    currentDate = now.strftime("%b %d")
    
    # if DEBUG:
    #   print(len(currentTime) * HEADING_CHAR_WIDTH + (2*SPACING))
    
    draw.text((SPACING, SPACING), currentTime, fill=BLACK, font=HEADING_FONT)
    
    # Find midpoint of the vertical space left
    
    
    draw.text((SPACING, (2*SPACING) + HEADING_SIZE), currentDay, fill=BLACK, font=REGULAR_FONT)
    draw.text((SPACING, (3*SPACING) + HEADING_SIZE + REGULAR_SIZE), currentDate, fill=BLACK, font=REGULAR_FONT)
    
    # composite.UpdateText(IDS.TIME.value, currentTime, BOLD_FONT_PATH)
    # composite.UpdateText(IDS.DAY.value, currentDay, REGULAR_FONT_PATH)
    # composite.UpdateText(IDS.DATE.value, currentDate, REGULAR_FONT_PATH)
  
  # Weather Update
  if(now.minute % 30 == 0 or firstUpdate):
    # composite.UpdateImg(IDS.WEATHER_ICON.value, WEATHER_ICON_BASE + currentWeatherIcon)
    # composite.UpdateText(IDS.TEMP.value, "21\u00b0C", REGULAR_FONT_PATH)
    # composite.UpdateText(IDS.TEMP_RANGE.value, "17\u00b0C/21\u00b0C", REGULAR_FONT_PATH)
    # draw.
    pass

if __name__ == "__main__":
  try:
    init()
    main()
  finally:
    if(DEBUG):
      print("Ending...")
    deinit()
