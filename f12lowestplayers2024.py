from ppadb.client import Client
import subprocess
from PIL import Image 
import pytesseract
import time 
import numpy
import os
import cv2
#changes to jeddah and 7 laps races strat
import random

os.environ["TESSDATA_PREFIX"] = 'C:/Users/seeho/testadb/misc/Tesseract-OCR/tessdata'
adb = Client(host='127.0.0.1', port= 5037)
devices = adb.devices()
start_time = time.time()
if len(devices) == 0:
    print('no device attached')
    quit()



device = devices[0]

# Capture a screenshot and save it
boost_time = random.uniform(0.2, 0.5)
sleep_time = random.uniform(0.5, 2.0)
sleep_time2 = random.uniform(1.5, 3.0)
state = 100
wet = 0
barca = 0
jeddah = 0
winner1 = 0
race = 0
lecwet = 0
sprint = 0
last_rain_change_time = 0  # Track the last time rain status changed
is_raining = False  # Track the current rain status
# Check if the extracted text is "7"
while True:
    time.sleep(0.1)
    image = device.screencap()

    with open('screen.png', 'wb') as f:
        f.write(image)

    # image = Image.open('screen.png')
    # image = numpy.array(image, dtype=numpy.uint8)
    # logo = Image.open('cloud.png')
    # logo = numpy.array(image, dtype=numpy.uint8)
    
    image = cv2.imread('screen.png')
    cloud = cv2.imread('cloud.png')
    lap4 = cv2.imread('lap4.jpg')
    lap7 = cv2.imread('lap7.jpg')
    lightrain = cv2.imread('lightrain.jpg')
    lap10 = cv2.imread('lap10.jpg')
    winner = cv2.imread('winner.jpg')
    crate = cv2.imread('crate.jpg')
    heavyrain = cv2.imread('heavyrain.jpg')
    lap8 = cv2.imread('lap8.jpg')

    cloudres = cv2.matchTemplate(image, cloud, cv2.TM_CCOEFF_NORMED)
    lap4res = cv2.matchTemplate(image, lap4, cv2.TM_CCOEFF_NORMED)
    lap8res = cv2.matchTemplate(image, lap8, cv2.TM_CCOEFF_NORMED)
    lap7res = cv2.matchTemplate(image, lap7, cv2.TM_CCOEFF_NORMED)
    lightrainres = cv2.matchTemplate(image, lightrain, cv2.TM_CCOEFF_NORMED)
    lap10res = cv2.matchTemplate(image, lap10, cv2.TM_CCOEFF_NORMED)
    winnerres = cv2.matchTemplate(image, winner, cv2.TM_CCOEFF_NORMED)
    crateres = cv2.matchTemplate(image, crate, cv2.TM_CCOEFF_NORMED)
    heavyrainres = cv2.matchTemplate(image, heavyrain, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9

    cloudloc = numpy.where(cloudres >= threshold)
    for pt in zip(*cloudloc[::-1]):
        bottom_right = (pt[0] + cloud.shape[1], pt[1] + cloud.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    lap4loc = numpy.where(lap4res >= threshold)
    for pt in zip(*lap4loc[::-1]):
        bottom_right = (pt[0] + lap4.shape[1], pt[1] + lap4.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    lap8loc = numpy.where(lap8res >= threshold)
    for pt in zip(*lap8loc[::-1]):
        bottom_right = (pt[0] + lap8.shape[1], pt[1] + lap8.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    lap7loc = numpy.where(lap7res >= threshold)
    for pt in zip(*lap7loc[::-1]):
        bottom_right = (pt[0] + lap7.shape[1], pt[1] + lap7.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    lightrainloc = numpy.where(lightrainres >= threshold)
    for pt in zip(*lightrainloc[::-1]):
        bottom_right = (pt[0] + lightrain.shape[1], pt[1] + lightrain.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    lap10loc = numpy.where(lap10res >= threshold)
    for pt in zip(*lap10loc[::-1]):
        bottom_right = (pt[0] + lap10.shape[1], pt[1] + lap10.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    winnerloc = numpy.where(winnerres >= threshold)
    for pt in zip(*winnerloc[::-1]):
        bottom_right = (pt[0] + winner.shape[1], pt[1] + winner.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    crateloc = numpy.where(crateres >= threshold)
    for pt in zip(*crateloc[::-1]):
        bottom_right = (pt[0] + crate.shape[1], pt[1] + crate.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    heavyrainloc = numpy.where(heavyrainres >= threshold)
    for pt in zip(*heavyrainloc[::-1]):
        bottom_right = (pt[0] + heavyrain.shape[1], pt[1] + heavyrain.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)
    
    # # Perform OCR on the screenshot
    pytesseract.pytesseract.tesseract_cmd = 'C:/Users/seeho/testadb/misc/Tesseract-OCR/tesseract.exe'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray, lang='eng', config='--psm 6 tessedit_char_unblacklist=0123456789')
    # cv2.imwrite('output.png', image)
    # Print the extracted text

    print(extracted_text)
    # print(lap8loc[0].size)
    # print("cloud:{}", cloudloc[0].size)
    print(state)
    # Clean up the screenshot file
    # os.remove('screen.png')
    # Example for when it starts raining
    if ("power-ups" in extracted_text or "POWER-UP EXPIRED" in extracted_text):
        device.shell('input touchscreen tap 460 1607')
        
    if "Not sure yet It's great!" in extracted_text:
        device.shell('input touchscreen tap 300 1315')
        print("dismissed rating")
    if "Rain" in extracted_text and not is_raining:
        is_raining = True
        last_rain_change_time = time.time()  # Update the time when the rain status changed

    # Example for when it stops raining
    if "Rain" not in extracted_text and is_raining:
        is_raining = False
        last_rain_change_time = time.time()  # Update the time when the rain status changed
    if state == 100 and ("Unavailable" in extracted_text or "REWARDS" in extracted_text or "Bonus" in extracted_text):
        #race
        device.shell('input touchscreen tap 560 1607')
        print("race")
        time.sleep(1.5)
        #Duels
        device.shell('input touchscreen tap 551 540')
        time.sleep(sleep_time)
        print("duels")
        #slide right
        device.shell('input swipe 200 1300 600 1300 1000')
        time.sleep(sleep_time)
        # device.shell('input swipe 200 1300 600 1300 1000')
        time.sleep(sleep_time2)
        device.shell('input touchscreen tap 580 1850')
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 550 1485')
        time.sleep(sleep_time)
        state = 101

    elif state == 101 and "ZANDVOORT" in extracted_text:
        time.sleep(22)
        state = 30
        print("ZANDVOORT")

    elif state == 101 and ("MIAMI" in extracted_text or "AUTODROME" in extracted_text):
        time.sleep(20)
        state = 150
        print("MIAMI")

    elif state == 101 and ("DHABI" in extracted_text or "SILVERSTONE" in extracted_text or "UNITED KINGDOM" in extracted_text):
        time.sleep(20)
        state = 80
        print("ABU")

    elif state == 101 and ("SINGAPORE" in extracted_text or "MEXICO" in extracted_text or "BARCELONA" in extracted_text):
        time.sleep(25)
        state = 20
        print("SINGAPORE")

    elif state == 101 and "STAVELOT" in extracted_text:
        time.sleep(20)
        state = 70
        print("STAVELOT")

    elif state == 101 and ("HUNGARY" in extracted_text or "MOGYOROD" in extracted_text):
        time.sleep(20)
        state = 200
        print("HUNGARY")
    
    elif state == 101 and "MEXICO" in extracted_text:
        time.sleep(25)
        state = 200
        print("Mexico City")
            
    #num of laps race pg

    elif state == 101 and "MONTREAL" in extracted_text:
        time.sleep(25)
        state = 200
        print("MONTREAL")

    elif state == 101 and "MONACO" in extracted_text:
        time.sleep(20)
        state = 200
        print("MONACO")
    
    elif state == 101 and "VEGAS" in extracted_text:
        time.sleep(20)
        state = 150
        print("JEDDAH now VEGAS")
    
    elif state == 101 and "PAULO" in extracted_text:
        time.sleep(25)
        state = 60
        print("SAO PAULO")

    elif cloudloc[0].size > 0 and state == 80:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 81

    elif cloudloc[0].size == 0 and state == 80:
        print("lap8")
        #lecmedium
        device.shell('input touchscreen tap 300 956')
        time.sleep(sleep_time)
        #PIA Hards
        device.shell('input touchscreen tap 900 1150')
        time.sleep(sleep_time)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 81

    elif cloudloc[0].size > 0 and state == 60:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 61

    elif cloudloc[0].size == 0 and state == 60:
        print("lap8")
        #lecsoft
        device.shell('input touchscreen tap 300 1156')
        time.sleep(sleep_time)
        #PIA medium
        device.shell('input touchscreen tap 900 1150')
        time.sleep(sleep_time)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 61

    elif cloudloc[0].size > 0 and state == 70:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 71

    elif cloudloc[0].size == 0 and state == 70:
        print("lap8")
        #lechards
        device.shell('input touchscreen tap 300 1350')
        time.sleep(sleep_time)
        #PIA Hards
        device.shell('input touchscreen tap 900 1350')
        time.sleep(sleep_time)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 71

    elif cloudloc[0].size > 0 and state == 20:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 21

    elif cloudloc[0].size == 0 and state == 20:
        print("lap8")
        #lecmedium
        device.shell('input touchscreen tap 300 1356')
        time.sleep(sleep_time)
        #PIA Hards
        device.shell('input touchscreen tap 900 1350')
        time.sleep(sleep_time)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 21

    elif cloudloc[0].size > 0 and state == 30:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 31

    elif cloudloc[0].size == 0 and state == 30:
        print("lap8")
        #lecmedium
        device.shell('input touchscreen tap 300 1356')
        time.sleep(sleep_time)
        #PIA Hards
        device.shell('input touchscreen tap 900 1350')
        time.sleep(sleep_time)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 31

    elif cloudloc[0].size > 0 and state == 150:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 151

    elif cloudloc[0].size == 0 and state == 150:
        print("lap8")
        #lecmedium
        device.shell('input touchscreen tap 300 950')
        time.sleep(sleep_time)
        #PIA Hards
        device.shell('input touchscreen tap 900 1150')
        time.sleep(sleep_time)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 151

    elif state == 101 and lap4loc[0].size > 0:
        if cloudloc[0].size > 0:
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 0
            wet = 1
        else:
            print("lap8")
            #lecmedium
            device.shell('input touchscreen tap 300 956')
            time.sleep(sleep_time)
            #PIA hards
            device.shell('input touchscreen tap 900 950')
            time.sleep(sleep_time)
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 0
            barca = 1

    elif state == 101 and lap8loc[0].size > 0:
        if cloudloc[0].size > 0:
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 201
            wet = 1
        else:
            print("lap8")
            #lecmedium
            device.shell('input touchscreen tap 300 956')
            time.sleep(sleep_time)
            #PIA hards
            device.shell('input touchscreen tap 900 950')
            time.sleep(sleep_time)
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 201
            barca = 1

    elif state == 101 and lap10loc[0].size > 0:
        if cloudloc[0].size > 0:
            time.sleep(2)
            device.shell('input touchscreen tap 588 2250')
            state = 10
        else:
            #lecmedium
            time.sleep(2)
            device.shell('input touchscreen tap 300 1356')
            time.sleep(sleep_time)
            #PIA hards
            device.shell('input touchscreen tap 900 1350')
            time.sleep(sleep_time)
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 10
            print("SPIELBERG")

    elif state == 101 and lap4loc[0].size > 0:
        if cloudloc[0].size > 0:
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 0
            wet = 1
        else:
            print("lap8")
            #lecmedium
            device.shell('input touchscreen tap 300 956')
            time.sleep(sleep_time)
            #PIA hards
            device.shell('input touchscreen tap 900 950')
            time.sleep(sleep_time)
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 0
            barca = 1
            
    #check for num of laps and rain
    elif state == 101 and lap7loc[0].size > 0:
        if (cloudloc[0].size > 0 or heavyrainloc[0].size > 0):
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 2000
            wet = 1
            

        else:
            print("lap7")
            #lechards
            device.shell('input touchscreen tap 300 1356')
            time.sleep(sleep_time)
            #PIA hards
            device.shell('input touchscreen tap 900 1350')
            time.sleep(sleep_time)
            #start race
            device.shell('input touchscreen tap 588 2250')
            time.sleep(4)
            state = 2000
            jeddah = 1

    elif state == 2000 and ("1/7" in extracted_text or "LAP1" in extracted_text or "LAP 1" in extracted_text or "/7" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 200 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        # time.sleep(boost_time)
        # device.shell('input touchscreen tap 1000 1480')
        # time.sleep(15)
        # device.shell('input touchscreen tap 120 1630')
        # time.sleep(8)
        # device.shell('input touchscreen tap 990 1630')
        
        print("success")
        state = 0.1
        print(state)

    elif state == 0.1 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "Rain" in extracted_text and "/7" in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(4)
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)
        time.sleep(20)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.2
        wet = 1

    elif state == 0.2 and wet == 0 and "LAP 4" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text) and "/7" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(4)
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.3
        lecwet = 1
        wet = 1
    elif state == 0.1 and wet == 0 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "/7" in extracted_text:
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #PIAsoft
        device.shell('input touchscreen tap 230 1569')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        #boost pia
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(sleep_time)
        #lecsoft
        device.shell('input touchscreen tap 820 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        # device.shell('input touchscreen tap 1000 1480')
        state = 0.2
        
    elif state == 0.2 and wet == 0 and ("LAP5" in extracted_text or "LAP 5" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text) and "/7" in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 2050')
        time.sleep(2)
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(sleep_time)
        time.sleep(20)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.4
        wet = 1
    elif state == 0.2 and wet == 1 and ("LAP5" in extracted_text or "LAP 5" in extracted_text) and ("Rain" in extracted_text or is_raining or "rain" in extracted_text or (time.time() - last_rain_change_time) < 60) and "/7" in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 2050')
        time.sleep(2)
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(sleep_time)
        time.sleep(20)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.4
        wet = 1
    elif state == 0.2 and ("LAP5" in extracted_text or "LAP 5" in extracted_text or "LAPS" in extracted_text)  and "5/7" in extracted_text and "Starts" not in extracted_text and "Rain" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(sleep_time)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 2050')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #PIAmed
        device.shell('input touchscreen tap 230 1569')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(5)
        state = 0.4

    elif state == 0.4 and lecwet == 1 and "LAP 6" in extracted_text and "Rain" in extracted_text and "/7" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 2045')
        time.sleep(sleep_time)
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.5
        wet = 1

    elif state == 0.4 and ("7/7" in extracted_text or "/7" in extracted_text):
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(boost_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')

    elif (state == 0.4 or state == 0.5) and "7/7" in extracted_text:
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        

    #Lap 8
    elif state == 0 and ("1/4" in extracted_text or "LAP1" in extracted_text or "LAP 1" in extracted_text or "/8" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        #lec boost again
        time.sleep(55)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(2)
        #stop lec boost
        device.shell('input touchscreen tap 110 1530')
        # time.sleep(13)
        # device.shell('input touchscreen tap 109 1618')
        # time.sleep(sleep_time)
        # device.shell('input touchscreen tap 110 1418')
        print("success")
        state = 1
    elif state == 1 and ("LAP 2" in extracted_text or "LAP2" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text) and "/8" in extracted_text:
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 2
        wet = 1
        print('test lap 3')

    elif state == 1 and ("LAP 2" in extracted_text or "LAP2" in extracted_text) and "Rain" not in extracted_text:
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #PIAsofts
        device.shell('input touchscreen tap 230 1569')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(sleep_time)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(sleep_time)
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 2
        wet = 0
            
    elif (state == 2 or state == 3) and ("4/4" in extracted_text or "/4" in extracted_text):
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(boost_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')

    #Lap 8
    elif state == 201 and ("1/8" in extracted_text or "LAP1" in extracted_text or "LAP 1" in extracted_text or "/8" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        #lec boost again
        time.sleep(55)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(2)
        #stop lec boost
        device.shell('input touchscreen tap 110 1530')
        # time.sleep(13)
        # device.shell('input touchscreen tap 109 1618')
        # time.sleep(sleep_time)
        # device.shell('input touchscreen tap 110 1418')
        print("success")
        state = 202
    elif state == 202 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text) and "/8" in extracted_text:
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 203
        wet = 1
        print('test lap 3')

    elif state == 202 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "Rain" not in extracted_text and "Light" not in extracted_text:
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #PIAsofts
        device.shell('input touchscreen tap 230 1569')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(sleep_time)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
       
        state = 203
        wet = 0

    elif state == 203 and wet == 0 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text) and "/8" in extracted_text:
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        #lec pitstop
        time.sleep(3)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 204
        wet = 1
    #raining but previously car not fitted with wets
    elif state == 203 and wet == 0 and ("LAP5" in extracted_text or "LAP 5" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        
        wet = 1
        state = 204
        print("lol")
    

    elif state == 203 and wet == 1 and ("LAP5" in extracted_text or "LAP 5" in extracted_text) and "Rain" in extracted_text and "/8" in extracted_text:
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 204
        wet = 1
        print("lol")

    elif state == 203 and ("LAP5" in extracted_text or "LAP 5" in extracted_text or "LAPS" in extracted_text) and "Rain" not in extracted_text and "/8" in extracted_text and "Starts" not in extracted_text and "LAP4" not in extracted_text and "LAP 4" not in extracted_text and "LAP3" not in extracted_text and "LAP 3" not in extracted_text:
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #PIA hard
        device.shell('input touchscreen tap 302 1960')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(sleep_time)
        #lecmhards
        device.shell('input touchscreen tap 852 1971')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 2050')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        
        state = 204
        wet = 0

    elif state == 203 and wet == 0 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and "Rain" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(3)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(8)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 204
        wet = 1

    elif state == 203 and wet == 0 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and "Rain" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 204
        wet = 1

    elif state == 203 and wet == 1 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and "Rain" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 204
        wet = 1

    elif state == 204 and wet == 0 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and "Rain" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 205
        wet = 1

    

    elif state == 203 and wet == 1 and "LAP 6" in extracted_text and "/8" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(sleep_time)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIAsofts
        device.shell('input touchscreen tap 230 1569')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 204
        wet = 0
            
    elif (state == 204 or state == 205) and ("8/8" in extracted_text or "/8" in extracted_text):
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(boost_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')

    #previously JEDDAH now Las Vegas
    elif state == 151 and ("1/6" in extracted_text or "LAP1" in extracted_text or "LAP 1" in extracted_text or "/6" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        # time.sleep(10)
        # device.shell('input touchscreen tap 120 1630')
        # time.sleep(10)
        # device.shell('input touchscreen tap 990 1630')
        
        print("success")
        state = 152
        print(state)

    elif state == 152 and ("LAP 2" in extracted_text or "LAP2" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        #lec pitstop
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 153
        wet = 1

    elif state == 152 and ("LAP 2" in extracted_text or "LAP2" in extracted_text) and "Rain" not in extracted_text and "rain" not in extracted_text and "LAP1" not in extracted_text and "LAP 1" not in extracted_text and "1/6" not in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 302 1571')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(2)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(1.5)
        #PIA medium
        device.shell('input touchscreen tap 852 1760')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 153

    elif state == 153 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(10)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 155
        wet = 1

    elif state == 153 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and "Rain" not in extracted_text and "rain" not in extracted_text and "LAP3" not in extracted_text and "LAP 3" not in extracted_text and "3/6" not in extracted_text:
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecmedium
        device.shell('input touchscreen tap 302 1571')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(2)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIA hard
        device.shell('input touchscreen tap 820 1760')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(10)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 155

    elif state == 155 and ("LAP 6" in extracted_text or "LAP6" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(15)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 156
        wet = 1

    # elif state == 155 and "LAP6" in extracted_text and "Rain" not in extracted_text:
    #     #lec pitstop
    #     time.sleep(sleep_time)
    #     device.shell('input touchscreen tap 216 2265')
    #     time.sleep(sleep_time)
    #     #lecsoft
    #     device.shell('input touchscreen tap 302 1571')
    #     time.sleep(sleep_time)
    #     # #lecserv
    #     device.shell('input touchscreen tap 290 2050')
    #     time.sleep(5)
    #     #boost lec
    #     device.shell('input touchscreen tap 110 1480')
    #     time.sleep(sleep_time)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 820 2270')
    #     time.sleep(sleep_time)
    #     #PIAmed
    #     device.shell('input touchscreen tap 852 1565')
    #     time.sleep(sleep_time)
    #     # #PIAserv
    #     device.shell('input touchscreen tap 836 2050')
    #     time.sleep(sleep_time)
    #     #boost pia
    #     device.shell('input touchscreen tap 1000 1480')
    #     state = 157

    elif (state == 157 or state == 155) and "/6" in extracted_text:
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')

    #spielberg
    elif state == 10 and ("1/5" in extracted_text or "/5" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        state = 11
    
    elif state == 11 and "LAP 4" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text):
        time.sleep(5)
        #lec pitstop
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(20)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 12
        wet = 1

    elif state == 11 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecmedium
        device.shell('input touchscreen tap 230 1765')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(3)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIAmed
        device.shell('input touchscreen tap 820 1769')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 12
        wet = 0

    elif state == 13 and "10/10" in extracted_text:
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        state = 13

    #Singapore
    elif state == 21 and ("1/6" in extracted_text or "/6" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        # time.sleep(5)
        # device.shell('input touchscreen tap 990 1530')
        # time.sleep(7)
        # device.shell('input touchscreen tap 120 1530')
        time.sleep(10)
        # device.shell('input touchscreen tap 950 795')
        
        print("success")
        state = 22
        print(state)
    elif state == 22 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        # device.shell('input touchscreen tap 110 1480')
        time.sleep(5)
        #lec pitstop
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        # device.shell('input touchscreen tap 1000 1480')
        state = 23
        wet = 1
    elif state == 22 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "Rain" not in extracted_text and "Light" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 302 1971')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIA medium
        device.shell('input touchscreen tap 852 1960')
        time.sleep(sleep_time)
        time.sleep(26)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 23
        wet = 0

    elif state == 23 and wet == 0 and "LAP 4" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text) and "Sunny" not in extracted_text and "Partly" not in extracted_text:
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(5)
        #lec pitstop
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 24
        wet = 1

    # elif state == 23 and ("LAP 5" in extracted_text or "LAP5" in extracted_text or "LAPS" in extracted_text) and "Rain" not in extracted_text and "Light" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60 and "5/6" in extracted_text:
    #     time.sleep(sleep_time)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 216 2270')
    #     time.sleep(sleep_time)
    #     #PIAsofts
    #     device.shell('input touchscreen tap 230 1565')
    #     time.sleep(sleep_time)
    #     # #PIAserv
    #     device.shell('input touchscreen tap 290 2050')
    #     time.sleep(2)
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     #lec pitstop
    #     time.sleep(sleep_time)
    #     device.shell('input touchscreen tap 820 2265')
    #     time.sleep(sleep_time)
    #     #lecsofts
    #     device.shell('input touchscreen tap 820 1565')
    #     time.sleep(sleep_time)
    #     # #lecserv
    #     device.shell('input touchscreen tap 836 2050')
    #     time.sleep(sleep_time)
    #     #boost lec
    #     device.shell('input touchscreen tap 1000 1480')
    #     state = 24

    elif (state == 23 or state == 24) and "6/6" in extracted_text and "Rain" not in extracted_text:
        time.sleep(boost_time)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        
    #ZANDVOORT
    elif state == 31 and ("1/7" in extracted_text or "/7" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(25)
        device.shell('input touchscreen tap 990 1630')
        time.sleep(5)
        device.shell('input touchscreen tap 120 1630')
        
        print("success")
        state = 32

    elif state == 32 and "LAP 4" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text):
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 33
        wet = 1

    elif state == 32 and ("LAP 4" in extracted_text or "LAP4" in extracted_text):
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecsoft
        device.shell('input touchscreen tap 302 1771')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(3)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIA medium
        device.shell('input touchscreen tap 852 1760')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 33
        wet = 0

    elif state == 33 and wet == 0 and "LAP5" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text):
        time.sleep(5)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 2050')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 34
        wet = 1

    # elif state == 33 and wet == 1 and "LAP5" in extracted_text and "Rain" in extracted_text:
    #     state = 34
    
    elif state == 33 and wet == 1 and "LAP5" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 230 1765')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIAmed
        device.shell('input touchscreen tap 820 1769')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 34
        wet = 0
    
    elif state == 33 and "7/7" in extracted_text:
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
    elif state == 34 and "7/7" in extracted_text:
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')

    #BRAZIL SAO PAULO
    elif state == 61 and ("1/9" in extracted_text or "/9" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        state = 62
    
    elif state == 62 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        time.sleep(5)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(20)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 63
        wet = 1

    elif state == 62 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 230 1765')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(3)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIAmed
        device.shell('input touchscreen tap 820 1769')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 63
        wet = 0

    elif state == 63 and ("LAP 6" in extracted_text or "LAP6" in extracted_text) and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 230 1765')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(3)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIAmed
        device.shell('input touchscreen tap 820 1769')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 64
        wet = 0

    elif state == 64 and "LAP 8" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text):
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(2)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 820 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 65
        wet = 1
    elif state == 65 and "9/9" in extracted_text:
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        state = 65
        
    elif state == 64 and "9/9" in extracted_text:
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        state = 64

    #SPA
    elif state == 71 and ("1/6" in extracted_text or "/6" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(5)
        device.shell('input touchscreen tap 990 1630')
        time.sleep(6)
        device.shell('input touchscreen tap 120 1630')
        time.sleep(4)
        device.shell('input touchscreen tap 950 795')
        
        print("success")
        state = 72
        print(state)
    elif state == 72 and ("LAP 2" in extracted_text or "LAP2" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #stop pia boost
        device.shell('input touchscreen tap 110 1630')
        time.sleep(0.1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #lec pitstop
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(6)
        #stop pia boost
        device.shell('input touchscreen tap 110 1630')
        state = 73
        wet = 1
        
    # elif state == 73 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
    #     time.sleep(sleep_time)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 216 2270')
    #     time.sleep(1.5)
    #     #pia wets
    #     device.shell('input touchscreen tap 300 2122')
    #     time.sleep(1.5)
    #     #PIAserv
    #     device.shell('input touchscreen tap 290 1856')
    #     time.sleep(sleep_time)        
    #     #boost lec
    #     device.shell('input touchscreen tap 1000 1480')
    #     time.sleep(2)
    #     #stop pia boost
    #     device.shell('input touchscreen tap 110 1630')
       
    #     state = 74
    #     wet = 1
    elif state == 72 and "LAP 2" in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 230 1771')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(1.5)
        #PIA medium
        device.shell('input touchscreen tap 820 1760')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 73
        wet = 0

    # elif state == 73 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "Rain" not in extracted_text:
    #     #lec pitstop
    #     time.sleep(sleep_time)
    #     device.shell('input touchscreen tap 216 2265')
    #     time.sleep(2)
    #     #lecmedium
    #     device.shell('input touchscreen tap 230 1971')
    #     time.sleep(1.5)
    #     #lecserv
    #     device.shell('input touchscreen tap 290 1856')
    #     time.sleep(sleep_time)
    #     time.sleep(25)
    #     #boost lec
    #     device.shell('input touchscreen tap 110 1480')
    #     state = 74
    #     wet = 0

    elif state == 73 and wet == 1 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        # time.sleep(sleep_time)
        #lec pitstop
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        
        state = 75
        wet = 1

    elif state == 73 and wet == 0 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        # time.sleep(5)
        #lec pitstop
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 75
        wet = 1

    elif state == 73 and ("LAP 4" in extracted_text or "LAP4" in extracted_text):
        time.sleep(sleep_time)
        #stop lec boost
        device.shell('input touchscreen tap 110 1630')
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 230 1765')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(1.5)
        #PIA medium
        device.shell('input touchscreen tap 820 1760')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        #lec pitstop
        time.sleep(30)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        time.sleep(2)
        
        state = 75
        wet = 0

    elif state == 75 and ("6/6" in extracted_text or "/6" in extracted_text):
        time.sleep(boost_time)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        

    elif state == 74 and "Rain" in extracted_text and ("LAP 6" in extracted_text or "/6" in extracted_text):
        # #boost LEC
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost PIA
        device.shell('input touchscreen tap 1000 1480')
        state = 1000
    #Abu Dhabi
    elif state == 81 and ("1/5" in extracted_text or "LAP1" in extracted_text or "LAP 1" in extracted_text or "/8" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        # time.sleep(13)
        # device.shell('input touchscreen tap 109 1618')
        # time.sleep(sleep_time)
        # device.shell('input touchscreen tap 110 1418')
        print("success")
        state = 82
    elif state == 82 and "LAP 2" in extracted_text and "Rain" in extracted_text and "/5" in extracted_text:
        time.sleep(5)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 83
        wet = 1
        print('test lap 3')

    elif state == 82 and ("LAP 2" in extracted_text or "LAP2" in extracted_text) and "/5" in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecsofts
        device.shell('input touchscreen tap 230 1565')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIAmed
        device.shell('input touchscreen tap 820 1769')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(15)
        device.shell('input touchscreen tap 120 1530')
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 990 1530')
        state = 83
        wet = 0

    elif state == 83 and wet == 0 and "LAP 4" in extracted_text and "Rain" in extracted_text and "/5" in extracted_text:
        time.sleep(4)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)
        #lec pitstop
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 84
        wet = 1

    elif state == 83 and wet == 0 and "LAP4" in extracted_text and "Rain" in extracted_text and "/5" in extracted_text:
        
        time.sleep(5)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #lec pitstop
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 84
        print("lol")

    elif state == 83 and ("LAP4" in extracted_text or "LAP 4" in extracted_text) and "/5" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecmed
        device.shell('input touchscreen tap 230 1565')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIAmed
        device.shell('input touchscreen tap 820 1569')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 84
        wet = 0
            
    elif state == 84 and ("5/5" in extracted_text and "/5" in extracted_text):
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 84
    

    elif "Debrief" in extracted_text or "WINNER" in extracted_text or "Activate now" in extracted_text or "Standard" in extracted_text or "RESULTS" in extracted_text:
        if (crateloc[0].size > 0 or winnerloc[0].size > 0):
            winner1 += 1
            race += 1
            print(f"won: {winner1}")
            print(f"races: {race}")
            elapsed_time_seconds = time.time() - start_time
            hours, remainder = divmod(elapsed_time_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"Playing for {int(hours)} hours and {int(minutes)} minutes.")
            print(elapsed_time_seconds)
        else: 
            time.sleep(sleep_time)
            race += 1
            print(f"won: {winner1}")
            print(f"races: {race}")
            elapsed_time_seconds = time.time() - start_time
            hours, remainder = divmod(elapsed_time_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"Playing for {int(hours)} hours and {int(minutes)} minutes.")
            print(elapsed_time_seconds)
        time.sleep(2)
        device.shell('input touchscreen tap 857 2120')
        time.sleep(6)
        device.shell('input touchscreen tap 857 2250')
        time.sleep(0.5)
        device.shell('input touchscreen tap 580 2250')
        time.sleep(4)
        device.shell('input touchscreen tap 950 795')
        state = 100
        wet = 0
        lecwet = 0

    elif ("Continue" in extracted_text or "continue" in extracted_text or "POS. PLAYER Races TOTAL" in extracted_text):
        device.shell('input touchscreen tap 580 2120')
        time.sleep(sleep_time2)
        device.shell('input touchscreen tap 580 2250')
        time.sleep(sleep_time2)
        device.shell('input touchscreen tap 580 2250')
        time.sleep(4)
        device.shell('input touchscreen tap 950 795')
        state = 100

    elif "resume" in extracted_text:
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(boost_time)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')

    elif ("Safety car" in extracted_text or "safety car" in extracted_text):
        #boost LEC
        device.shell('input touchscreen tap 1000 1730')
        time.sleep(boost_time)
        #boost PIA
        device.shell('input touchscreen tap 110 1730')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 250 1830')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 350 1830')

    # elif "received a reward" in extracted_text:
    #     device.shell('input touchscreen tap 560 1600')
    #     time.sleep(4)
    #     device.shell('input touchscreen tap 560 1600')
    #     time.sleep(2)
    #     device.shell('input touchscreen tap 560 1600')
    #     time.sleep(2)
    #     device.shell('input touchscreen tap 560 1600')
    #     time.sleep(2)
    #     device.shell('input touchscreen tap 560 1600')
    #     time.sleep(2)
    #     device.shell('input touchscreen tap 560 1600')
    #     time.sleep(2)
    #     device.shell('input touchscreen tap 560 1600')
    #     time.sleep(8)
    #     device.shell('input touchscreen tap 300 2244')
    #     time.sleep(3)
    #     device.shell('input touchscreen tap 950 795')
    #     state = 100
    elif "received a reward" in extracted_text:
        device.shell('input touchscreen tap 560 1600')
        time.sleep(6)
        device.shell('input touchscreen tap 560 1600')
        time.sleep(4)
        device.shell('input touchscreen tap 560 1600')
        time.sleep(2)
        device.shell('input touchscreen tap 560 1600')
        time.sleep(2)
        device.shell('input touchscreen tap 560 1600')
        time.sleep(2)
        device.shell('input touchscreen tap 560 1600')
        time.sleep(2)
        device.shell('input touchscreen tap 560 1600')
        time.sleep(10)
        device.shell('input touchscreen tap 300 2244')
        time.sleep(5)
        device.shell('input touchscreen tap 950 795')
        time.sleep(0.5)
        sprint += 1
        print(f"opened crates: {sprint}")
        state = 100
        

