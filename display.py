from papirus import Papirus
from papirus import PapirusTextPos
from datetime import datetime
import time

textSize = 25
subtextSize = 15

updateFrame = False

prevMinute = -1
now = datetime.now()


def init():
  global screen, text

  screen = Papirus()
  screen.partial_update()
  text = PapirusTextPos(False)
  
  # TODO Move this to the screen switching code
  initStatus()
  
  text.WriteAll()
  
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
      text.WriteAll()
      updateFrame = False
    
    # Sleep
    time.sleep(1)
    
  
def initStatus():
  text.AddText(text=now.strftime("%H:%M"), x=5, y=10, size=textSize, Id="Time")
  text.AddText(text=now.strftime("%A"), x=5, y=textSize + 20, size=subtextSize, Id="Day")
  text.AddText(text=now.strftime("%b %d"), x=5, y=textSize + 20 + subtextSize, size=subtextSize, Id="Date")

def statusUpdate():
  global updateFrame
  
  if(prevMinute != now.minute): 
    print("time updated")
    updateFrame = True
    
    currentTime = now.strftime("%H:%M")
    currentDay = now.strftime("%A")
    currentDate = now.strftime("%b %d")
    
    text.UpdateText("Time", currentTime)
    text.UpdateText("Day", currentDay)
    text.UpdateText("Date", currentDate)
    

if __name__ == "__main__":
  init()
  main()
