# from time import sleep
# from papirus import PapirusText
# from papirus import Papirus
# from papirus import PapirusTextPos

# text = PapirusTextPos(False, rotation = 0)

from cgitb import text
from papirus import Papirus
from papirus import PapirusTextPos
from datetime import datetime
import time

textSize = 25
subtextSize = 15

updateFrame = False

prevMinute = 0
now = datetime.now()


def init():
  global screen, text

  screen = Papirus()
  text = PapirusTextPos(False)
  
  text.Clear()
  
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
    
    if updateFrame:
      text.WriteAll()
      updateFrame = False
    
    # Sleep
    time.sleep(1)
    
    # Update values
    prevMinute = now.minute
  
def initStatus():
  text.AddText(text="##:## XX", x=5, y=10, size=textSize, Id="Time")
  text.AddText(text="XXXXXX", x=5, y=textSize + 20, size=subtextSize, Id="Day")
  text.AddText(text="XXX ##", x=5, y=textSize + 20 + subtextSize, size=subtextSize, Id="Date")
  
def deInitStatus():
  text.RemoveText("Time")
  text.RemoveText("Date")

def statusUpdate():
  global updateFrame
  
  if(prevMinute != now.minute): 
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
