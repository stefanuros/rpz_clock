#!/usr/bin/env python3
from papirus import Papirus, PapirusComposite, LM75B
from datetime import datetime
import time
from keys import weatherApiKey
import geocoder
from PIL import Image, ImageDraw, ImageFont

TEXT_SIZE = 35
SUBTEXT_SIZE = 17

REGULAR_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

# REGULAR_FONT = ImageFont.truetype(REGULAR_FONT_PATH, TEXT_SIZE)
# REGULAR_CHAR_WIDTH = REGULAR_FONT.getsize("0")[0]
# BOLD_FONT = ImageFont.truetype(BOLD_FONT_PATH, SUBTEXT_SIZE)
# BOLD_CHAR_WIDTH = BOLD_FONT.getsize("0")[0]

WHITE, BLACK = 1, 0

updateFrame = False

prevMinute = -1
now = datetime.now()

def init():
  global text, screen, image, draw, sensor
  
  print("Starting...")

  text = PapirusComposite(False)
  text.partialUpdates = True
  screen = Papirus()
  text.partialUpdates = True
  image = Image.new('1', screen.size, WHITE)
  draw = ImageDraw.Draw(image)
  
  
  # TODO Move this to the screen switching code
  initStatus()
  
def deinit():
  text.Clear()
  
def main():
  global now, prevMinute, updateFrame
  
  while(True):
    # Get current time
    now = datetime.now()
    
    # Update the screen
    statusUpdate()
    
    # Update values
    prevMinute = now.minute
    
    if updateFrame:
      print("Main Update")
      text.WriteAll()
      updateFrame = False
    
    # Sleep
    time.sleep(1)
    
def initStatus():
  global updateFrame
  
  print("Status Init")
  text.AddText(text=now.strftime("%H:%M"), x=5, y=5, size=TEXT_SIZE, Id="Time", fontPath=BOLD_FONT_PATH)
  text.AddText(text=now.strftime("%A"), x=5, y=TEXT_SIZE + 15, size=SUBTEXT_SIZE, Id="Day", fontPath=REGULAR_FONT_PATH)
  text.AddText(text=now.strftime("%b %d"), x=5, y=TEXT_SIZE + 15 + SUBTEXT_SIZE, size=SUBTEXT_SIZE, Id="Date", fontPath=REGULAR_FONT_PATH)
  
  updateFrame = True

def statusUpdate():
  global updateFrame, text
  
  if(prevMinute != now.minute): 
    print("Status Update")
    updateFrame = True
    
    currentTime = now.strftime("%H:%M")
    currentDay = now.strftime("%A")
    currentDate = now.strftime("%b %d")
    
    text.UpdateText("Time", currentTime, BOLD_FONT_PATH)
    text.UpdateText("Day", currentDay, REGULAR_FONT_PATH)
    text.UpdateText("Date", currentDate, REGULAR_FONT_PATH)

if __name__ == "__main__":
  try:
    init()
    main()
  finally:
    print("Ending...")
    deinit()
