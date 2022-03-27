#!/usr/bin/env python3
from papirus import Papirus
from papirus import PapirusTextPos
from datetime import datetime
import time

textSize = 35
subtextSize = 15

updateFrame = False

prevMinute = -1
now = datetime.now()

boldFontPath = "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"
regularFontPath = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"


def init():
  global text
  
  print("Starting...")

  text = PapirusTextPos(False)
  text.partialUpdates = True
  
  # TODO Move this to the screen switching code
  initStatus()
  
def deinit():
  # TODO text has no attribute clear
  text.clear()
  
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
  text.AddText(text=now.strftime("%H:%M"), x=5, y=10, size=textSize, Id="Time", fontPath=boldFontPath)
  text.AddText(text=now.strftime("%A"), x=5, y=textSize + 20, size=subtextSize, Id="Day", fontPath=regularFontPath)
  text.AddText(text=now.strftime("%b %d"), x=5, y=textSize + 20 + subtextSize, size=subtextSize, Id="Date", fontPath=regularFontPath)
  
  updateFrame = True

def statusUpdate():
  global updateFrame, text
  
  if(prevMinute != now.minute): 
    print("Status Update")
    updateFrame = True
    
    currentTime = now.strftime("%H:%M")
    currentDay = now.strftime("%A")
    currentDate = now.strftime("%b %d")
    
    text.UpdateText("Time", currentTime, boldFontPath)
    text.UpdateText("Day", currentDay, regularFontPath)
    text.UpdateText("Date", currentDate, regularFontPath)

if __name__ == "__main__":
  try:
    init()
    main()
  finally:
    print("Ending...")
    deinit()
