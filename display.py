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

prevMinute = 0
now = datetime.now()


def init():
  global screen, text

  screen = Papirus()
  text = PapirusTextPos(False)
  
  text.Clear()
  
  # TODO Move this to the screen switching code
  initStatus()
  
def main():
  global now, prevMinute
  
  while(True):
    # Get current time
    now = datetime.now()
    
    # Update the screen
    statusUpdate()
    
    text.WriteAll()
    
    # Sleep
    time.sleep(1)
    
    # Update values
    prevMinute = now.minute
  
def initStatus():
  text.AddText(text="##:## XX", x=5, y=10, size=textSize, Id="Time")
  text.AddText(text="XXXXX, XXX ##", x=5, y=textSize + 20, size=subtextSize, Id="Day")
  text.AddText(text="XXXXX, XXX ##", x=5, y=textSize + 20 + subtextSize, size=subtextSize, Id="Date")
  
def deInitStatus():
  text.RemoveText("Time")
  text.RemoveText("Date")

def statusUpdate():
  if(prevMinute != now.minute): 
    currentTime = now.strftime("%H:%M")
    currentDay = now.strftime("%A")
    currentDate = now.strftime("%b %d")
    
    text.UpdateText("Time", currentTime)
    text.UpdateText("Date", currentDate)
    

if __name__ == "__main__":
  init()
  main()
