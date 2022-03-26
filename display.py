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
  text = PapirusTextPos()
  
  # TODO Move this to the screen switching code
  initStatus()
  
def main():
  global now, prevMinute
  
  while(True):
    # Get current time
    now = datetime.now()
    
    # Update the frame
    statusUpdate()
    
    # Sleep
    time.sleep(5)
    
    # Update values
    prevMinute = now.minute
  
def initStatus():
  text.AddText(text="##:## XX", x=5, y=5, size=textSize, Id="Time")
  text.AddText(text="XXXXX, XXX ##", x=5, y=textSize + 10, size=subtextSize, Id="Date")
  
def deInitStatus():
  text.RemoveText("Time")
  text.RemoveText("Date")

def statusUpdate():
  if(prevMinute != now.minute): 
    currentTime = now.strftime("%I:%M:%S %p")
    currentDate = now.strftime("%A, %b %d")
    
    text.UpdateText("Time", currentTime)
    text.UpdateText("Date", currentDate)
    

if __name__ == "__main__":
  init()
  main()
