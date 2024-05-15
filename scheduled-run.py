import time
import datetime

def job():
    print("working working. sir!")

while True:
    now = datetime.datetime.now()
    print(now)

    # every 1 second
    if now.second % 5 == 0:
        print("Hi. sec")

    # every 30 minutes
    if now.minute % 30 == 0:
        print("Ok. min")
    
    #  at mid-night
    if now.time() == datetime.time(0, 0):
        job()
    
    #  
    time.sleep(1)


