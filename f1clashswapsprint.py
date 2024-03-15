from ppadb.client import Client
import subprocess
from PIL import Image 
import pytesseract
import time 
import numpy
import os
import cv2
import random

#for two stop strat

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
sleep_time2 = random.uniform(2.0, 3.0)
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
    lap8 = cv2.imread('lap8.jpg')
    lap7 = cv2.imread('lap7.jpg')
    lightrain = cv2.imread('lightrain.jpg')
    lap10 = cv2.imread('lap10.jpg')
    winner = cv2.imread('winner.jpg')
    crate = cv2.imread('crate.jpg')
    heavyrain = cv2.imread('heavyrain.jpg')
    opencrate = cv2.imread('opencrate.jpg')

    opencrateres = cv2.matchTemplate(image, opencrate, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_crossloc = cv2.minMaxLoc(opencrateres)
    top_leftcross = max_crossloc
    heightcross, widthcross, _ = opencrate.shape
    center_x1 = top_leftcross[0] + widthcross // 2
    center_y1 = top_leftcross[1] + heightcross // 2

    

    cloudres = cv2.matchTemplate(image, cloud, cv2.TM_CCOEFF_NORMED)
    lap8res = cv2.matchTemplate(image, lap8, cv2.TM_CCOEFF_NORMED)
    lap7res = cv2.matchTemplate(image, lap7, cv2.TM_CCOEFF_NORMED)
    lightrainres = cv2.matchTemplate(image, lightrain, cv2.TM_CCOEFF_NORMED)
    lap10res = cv2.matchTemplate(image, lap10, cv2.TM_CCOEFF_NORMED)
    winnerres = cv2.matchTemplate(image, winner, cv2.TM_CCOEFF_NORMED)
    crateres = cv2.matchTemplate(image, crate, cv2.TM_CCOEFF_NORMED)
    heavyrainres = cv2.matchTemplate(image, heavyrain, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9

    opencrateloc = numpy.where(opencrateres >= threshold)
    for pt in zip(*opencrateloc[::-1]):
        bottom_right = (pt[0] + opencrate.shape[1], pt[1] + opencrate.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    cloudloc = numpy.where(cloudres >= threshold)
    for pt in zip(*cloudloc[::-1]):
        bottom_right = (pt[0] + cloud.shape[1], pt[1] + cloud.shape[0])
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
    # if "Open" in extracted_text:
    #     center_x_next = int(image.shape[1] / 2)  # Center of the image
    #     center_y_next = int(image.shape[0] / 2)  # Center of the image
    #     device.shell(f"input touchscreen tap {center_x_next} {center_y_next}")
    # Example for when it starts raining

    if "Rain" in extracted_text and not is_raining:
        is_raining = True
        last_rain_change_time = time.time()  # Update the time when the rain status changed

    # Example for when it stops raining
    if "Rain" not in extracted_text and is_raining:
        is_raining = False
        last_rain_change_time = time.time()  # Update the time when the rain status changed

    elif "Not sure yet It's great!" in extracted_text:
        device.shell('input touchscreen tap 300 1315')
        print("dismissed rating")

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
        # device.shell('input swipe 200 1300 600 1300 1000')
        time.sleep(sleep_time2)
        device.shell('input touchscreen tap 580 1300')
        time.sleep(sleep_time2)
        device.shell('input touchscreen tap 550 1485')
        time.sleep(sleep_time)
        state = 101

    elif state == 101 and "ZANDVOORT" in extracted_text:
        time.sleep(22)
        state = 30
        print("ZANDVOORT")

    elif state == 101 and ("MIAMI" in extracted_text or "AUTODROME" in extracted_text or "VEGAS" in extracted_text):
        time.sleep(20)
        state = 150
        print("MIAMI")

    # elif state == 101 and "DHABI" in extracted_text:
    #     time.sleep(20)
    #     state = 80
    #     print("ABU")

    elif state == 101 and "SINGAPORE" in extracted_text:
        time.sleep(25)
        state = 20
        print("SINGAPORE")

    elif state == 101 and "STAVELOT" in extracted_text:
        time.sleep(20)
        state = 70
        print("STAVELOT")

    elif state == 101 and ("HUNGARY" in extracted_text or "MOGYOROD" in extracted_text or "AUSTRALIA" in extracted_text):
        time.sleep(20)
        state = 200
        print("HUNGARY")
    
    elif state == 101 and "MEXICO" in extracted_text:
        time.sleep(25)
        state = 200
        print("Mexico City")
            
    #num of laps race pg
    elif state == 101 and "BARCELONA" in extracted_text:
        time.sleep(18)
        state = 200
        print("BARCA")

    elif state == 101 and "MONTREAL" in extracted_text:
        time.sleep(25)
        state = 200
        print("MONTREAL")

    elif state == 101 and "MONACO" in extracted_text:
        time.sleep(20)
        state = 200
        print("MONACO")
    
    elif state == 101 and "JEDDAH" in extracted_text:
        time.sleep(20)
        state = 150
        print("JEDDAH")
    
    elif state == 101 and "PAULO" in extracted_text:
        time.sleep(25)
        state = 60
        print("SAO PAULO")

    # elif state == 101 and "AUSTRALIA" in extracted_text:
    #     time.sleep(25)
    #     state = 109
    #     print("AUSTRALIA")

    elif cloudloc[0].size > 0 and state == 109:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 110

    elif cloudloc[0].size == 0 and state == 109:
        print("lap8")
        #lecmedium
        device.shell('input touchscreen tap 300 1356')
        time.sleep(sleep_time)
        #PIA Hards
        device.shell('input touchscreen tap 900 1150')
        time.sleep(sleep_time)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 110

    elif cloudloc[0].size > 0 and state == 80:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 81

    elif cloudloc[0].size == 0 and state == 80:
        print("lap8")
        #lecmedium
        device.shell('input touchscreen tap 300 1156')
        time.sleep(sleep_time)
        #PIA Hards
        device.shell('input touchscreen tap 900 1350')
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
        device.shell('input touchscreen tap 300 956')
        time.sleep(sleep_time)
        #PIA soft
        device.shell('input touchscreen tap 900 956')
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
        #lecsofts
        device.shell('input touchscreen tap 300 950')
        time.sleep(sleep_time)
        #PIA medium
        device.shell('input touchscreen tap 900 1150')
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
        #lecsofts
        device.shell('input touchscreen tap 300 956')
        time.sleep(sleep_time)
        #PIA medium
        device.shell('input touchscreen tap 900 1150')
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
        #lecsoft
        device.shell('input touchscreen tap 300 956')
        time.sleep(sleep_time)
        #PIA medium
        device.shell('input touchscreen tap 900 1150')
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
        #lecsoft
        device.shell('input touchscreen tap 300 950')
        time.sleep(sleep_time)
        #PIA medium
        device.shell('input touchscreen tap 900 1150')
        time.sleep(sleep_time)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 151

    elif cloudloc[0].size > 0 and state == 200:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 201

    elif cloudloc[0].size == 0 and state == 200:
        print("lap8")
        #lecmedium
        device.shell('input touchscreen tap 300 1156')
        time.sleep(sleep_time)
        #PIA medium
        device.shell('input touchscreen tap 900 1150')
        time.sleep(sleep_time)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 201

    elif state == 101 and lap8loc[0].size > 0:
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
            #PIA medium
            device.shell('input touchscreen tap 900 1150')
            time.sleep(sleep_time)
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 0
            barca = 1

    elif state == 101 and lap10loc[0].size > 0:
        if cloudloc[0].size > 0:
            time.sleep(2)
            device.shell('input touchscreen tap 588 2250')
            wet = 1
            state = 10
        else:
            #lecmedium
            time.sleep(2)
            device.shell('input touchscreen tap 300 1156')
            time.sleep(sleep_time)
            #PIA medium
            device.shell('input touchscreen tap 900 1150')
            time.sleep(sleep_time)
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 10
            print("SPIELBERG")

    elif state == 101 and lap8loc[0].size > 0:
        if cloudloc[0].size > 0:
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 0
            wet = 1
        else:
            print("lap8")
            #lecmedium
            device.shell('input touchscreen tap 300 1156')
            time.sleep(sleep_time)
            #PIA medium
            device.shell('input touchscreen tap 900 1150')
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
            #lecsoft
            device.shell('input touchscreen tap 300 956')
            time.sleep(sleep_time)
            #PIA medium
            device.shell('input touchscreen tap 900 1150')
            time.sleep(sleep_time)
            #start race
            device.shell('input touchscreen tap 588 2250')
            time.sleep(4)
            state = 2000
            jeddah = 1

    elif state == 2000 and ("1/7" in extracted_text or "LAP1" in extracted_text or "LAP 1" in extracted_text or "/7" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        # time.sleep(15)
        # device.shell('input touchscreen tap 120 1630')
        # time.sleep(8)
        # device.shell('input touchscreen tap 990 1630')
        
        print("success")
        state = 0.1
        print(state)

    elif state == 0.1 and wet == 1 and ("LAP 2" in extracted_text or "LAP2" in extracted_text) and "Rain" in extracted_text and "/7" in extracted_text:
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
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.2
        wet = 1

    elif state == 0.1 and ("LAP 2" in extracted_text or "LAP2" in extracted_text) and "/7" in extracted_text and "Rain" not in extracted_text and "LAP1" not in extracted_text and "LAP 1" not in extracted_text and "1/7" not in extracted_text:
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #PIAsoft
        device.shell('input touchscreen tap 230 1569')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 2050')
        #boost pia
        # #lec pitstop
        # time.sleep(sleep_time)
        # device.shell('input touchscreen tap 820 2265')
        # time.sleep(sleep_time)
        # #lecsoft
        # device.shell('input touchscreen tap 820 1565')
        # time.sleep(sleep_time)
        # #lecserv
        # device.shell('input touchscreen tap 836 1856')
        time.sleep(20)
        device.shell('input touchscreen tap 110 1480')
        # time.sleep(sleep_time)
        # device.shell('input touchscreen tap 1000 1480')
        state = 0.2

    elif state == 0.2 and wet == 0 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "Rain" in extracted_text and "/7" in extracted_text:
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
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.3
        wet = 1

    elif state == 0.2 and wet == 0 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "/7" in extracted_text and "Rain" not in extracted_text:
        # #PIA pitstop
        # device.shell('input touchscreen tap 216 2270')
        # time.sleep(sleep_time)
        # #PIAsoft
        # device.shell('input touchscreen tap 230 1569')
        # time.sleep(sleep_time)
        # #PIAserv
        # device.shell('input touchscreen tap 290 1856')
        # #boost pia
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(sleep_time)
        #lecsoft
        device.shell('input touchscreen tap 820 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(15)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 1000 1480')
        state = 0.3

    elif state == 0.3 and wet == 0 and "LAP 4" in extracted_text and (is_raining or "rain" in extracted_text or (time.time() - last_rain_change_time) < 60) and "/7" in extracted_text:
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
        state = 0.4
        lecwet = 1
        wet = 1

    elif state == 0.1 and wet == 1 and "LAP 4" in extracted_text and (is_raining or "rain" in extracted_text or (time.time() - last_rain_change_time) < 60) and "/7" in extracted_text:
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
        state = 0.4
        lecwet = 1
        wet = 1

    elif state == 0.3 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and "/7" in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #PIAmedium
        device.shell('input touchscreen tap 230 1769')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        #boost pia
        # #lec pitstop
        # time.sleep(sleep_time)
        # device.shell('input touchscreen tap 820 2265')
        # time.sleep(sleep_time)
        # #lecsoft
        # device.shell('input touchscreen tap 820 1565')
        # time.sleep(sleep_time)
        # #lecserv
        # device.shell('input touchscreen tap 836 1856')
        time.sleep(10)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 1000 1480')
        print((time.time() - last_rain_change_time))
        state = 0.4
        
    elif state == 0.4 and wet == 0 and ("LAP5" in extracted_text or "LAP 5" in extracted_text) and (is_raining or "rain" in extracted_text or (time.time() - last_rain_change_time) < 60) and "/7" in extracted_text:
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
        state = 0.5
        wet = 1
    elif (state == 0.3 or state == 0.2) and wet == 1 and ("LAP5" in extracted_text or "LAP 5" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text) and "/7" in extracted_text:
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
        state = 0.5
        wet = 1
    elif (state == 0.4) and ("LAP5" in extracted_text or "LAP 5" in extracted_text or "LAPS" in extracted_text) and "/7" in extracted_text and "Starts" not in extracted_text and "Rain" not in extracted_text:
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
        # #PIA pitstop
        # device.shell('input touchscreen tap 216 2270')
        # time.sleep(sleep_time)
        # #PIAmed
        # device.shell('input touchscreen tap 230 1569')
        # time.sleep(sleep_time)
        # #PIAserv
        # device.shell('input touchscreen tap 290 2050')
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(5)
        state = 0.5

    elif state == 0.3 and lecwet == 1 and "LAP 6" in extracted_text and "Rain" in extracted_text and "/7" in extracted_text and is_raining and (time.time() - last_rain_change_time) < 60:
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

    elif (state == 0.4 or state == 0.5) and ("7/7" in extracted_text or "/7" in extracted_text):
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        
    #Lap 8
    elif state == 0 and ("1/8" in extracted_text or "LAP1" in extracted_text or "LAP 1" in extracted_text or "/8" in extracted_text):
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
        device.shell('input touchscreen tap 110 1630')
        # time.sleep(13)
        # device.shell('input touchscreen tap 109 1618')
        # time.sleep(sleep_time)
        # device.shell('input touchscreen tap 110 1418')
        print("success")
        state = 1
    elif state == 1 and wet == 0 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
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
        lecwet = 1
        state = 3
        wet = 1
        print('test lap 3')
    elif state == 1 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecsoft
        device.shell('input touchscreen tap 230 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(10)
        #boost lec
        # device.shell('input touchscreen tap 110 1480')
        # time.sleep(sleep_time)
        # #PIA pitstop
        # device.shell('input touchscreen tap 216 2270')
        # time.sleep(sleep_time)
        # #PIAmed
        # device.shell('input touchscreen tap 230 1769')
        # time.sleep(sleep_time)
        # #PIAserv
        # device.shell('input touchscreen tap 290 1856')
        # time.sleep(sleep_time)
        # #boost pia
        # device.shell('input touchscreen tap 110 1480')
        state = 2
        wet = 0
    
    elif state == 2 and wet == 0 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text) and "/8" in extracted_text:
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
        state = 3
        wet = 1

    elif state == 1 and wet == 1 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text) and "/8" in extracted_text:
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
        state = 3
        wet = 1

    elif state == 2 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(sleep_time)
        #lecmedium
        device.shell('input touchscreen tap 820 1765')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(10)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        # time.sleep(sleep_time)
        # #PIA pitstop
        # device.shell('input touchscreen tap 216 2270')
        # time.sleep(sleep_time)
        # #PIAhards
        # device.shell('input touchscreen tap 230 1969')
        # time.sleep(sleep_time)
        # #PIAserv
        # device.shell('input touchscreen tap 290 1856')
        # time.sleep(sleep_time)
        # #boost pia
        # device.shell('input touchscreen tap 110 1480')
        state = 3
        wet = 0

    elif state == 3 and wet == 0 and ("LAP 5" in extracted_text or "LAP5" in extracted_text or "LAPS" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
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
        state = 4
        print("lol")

    elif state == 3 and wet == 1 and ("LAP 5" in extracted_text or "LAP5" in extracted_text or "LAPS" in extracted_text) and "/8" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(sleep_time)
        #lechard
        device.shell('input touchscreen tap 820 1765')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 2050')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #PIAhards
        device.shell('input touchscreen tap 230 1769')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 4
        wet = 0
    #raining but previously car not fitted with wets
    elif state == 3 and wet == 0 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
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
        state = 4
        print("lol")

    elif state == 3 and wet == 1 and lecwet == 1 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        
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
        state = 4
        wet = 1
        print("lol")
    
    # elif state == 3 and wet == 1 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
    #     time.sleep(sleep_time)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 216 2270')
    #     time.sleep(sleep_time)
    #     #pia wets
    #     device.shell('input touchscreen tap 300 2122')
    #     time.sleep(sleep_time)
    #     #PIAserv
    #     device.shell('input touchscreen tap 290 1856')
    #     time.sleep(8)        
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     #lec pitstop
    #     time.sleep(sleep_time)
    #     device.shell('input touchscreen tap 820 2265')
    #     #lec wets
    #     time.sleep(2)
    #     device.shell('input touchscreen tap 830 2146')
    #     time.sleep(sleep_time)
    #     #lecserv
    #     device.shell('input touchscreen tap 836 1856')
    #     time.sleep(3)
    #     #boost lec
    #     device.shell('input touchscreen tap 1000 1480')
    #     state = 4
    #     wet = 1

    elif state == 3 and wet == 0 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text) and "/8" in extracted_text:
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
        state = 4
        wet = 1

    elif (state == 3 or state == 4) and ("LAP 6" in extracted_text or "LAP6" in extracted_text) and "/8" in extracted_text and "Rain" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lechard
        device.shell('input touchscreen tap 230 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(25)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        # #PIA pitstop
        # device.shell('input touchscreen tap 216 2270')
        # time.sleep(sleep_time)
        # #PIAhards
        # device.shell('input touchscreen tap 230 1969')
        # time.sleep(sleep_time)
        # #PIAserv
        # device.shell('input touchscreen tap 290 1856')
        # time.sleep(sleep_time)
        # #boost pia
        # device.shell('input touchscreen tap 110 1480')
        state = 5
        wet = 0

    elif (state == 3 or state == 4 or state == 5) and wet == 1 and ("LAP7" in extracted_text or "LAP7" in extracted_text or "LAP?" in extracted_text) and "/8" in extracted_text and "Rain" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIAmed
        device.shell('input touchscreen tap 230 1569')
        time.sleep(1.5)
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
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 6
        wet = 0

    # elif (state == 4 or state == 5) and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and "Rain" not in extracted_text and "rain" not in extracted_text:
    #     time.sleep(boost_time)
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     #boost lec
    #     time.sleep(boost_time)
    #     device.shell('input touchscreen tap 1000 1480')
    #     time.sleep(sleep_time)
    #     # device.shell('input touchscreen tap 120 1630')
    #     # device.shell('input touchscreen tap 110 1630')
                    
    elif (state == 4 or state == 5 or state == 3) and ("8/8" in extracted_text or "/8" in extracted_text):
        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost lec
        # device.shell('input touchscreen tap 1000 1480')
    
        
    #Barcelona one stop
    elif state == 201 and ("1/8" in extracted_text or "LAP1" in extracted_text or "LAP 1" in extracted_text or "/8" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        # time.sleep(10)
        # device.shell('input touchscreen tap 120 1630')
        time.sleep(10)
        device.shell('input touchscreen tap 990 1630')
        print("success")
        state = 202

    elif state == 202 and "LAP 4" in extracted_text and (is_raining or "rain" in extracted_text or (time.time() - last_rain_change_time) < 45):
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
        time.sleep(10)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 203
        wet = 1

    elif state == 202 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and "LAP3" not in extracted_text and "LAP 3" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 45:
        # time.sleep(sleep_time)
        # #PIA pitstop
        # device.shell('input touchscreen tap 216 2270')
        # time.sleep(sleep_time)
        # #PIA med
        # device.shell('input touchscreen tap 302 1771')
        # time.sleep(sleep_time)
        # #PIAserv
        # device.shell('input touchscreen tap 290 1856')
        # time.sleep(sleep_time)
        # #boost pia
        # device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecmedium
        device.shell('input touchscreen tap 302 1770')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        state = 203
        wet = 0
    elif state == 203 and ("LAP5" in extracted_text or "LAP 5" in extracted_text or "LAPS" in extracted_text) and not is_raining:
        # time.sleep(sleep_time)
        # device.shell('input touchscreen tap 216 2265')
        # time.sleep(sleep_time)
        # #lecmedium
        # device.shell('input touchscreen tap 302 1770')
        # time.sleep(sleep_time)
        # #lecserv
        # device.shell('input touchscreen tap 290 1856')
        # time.sleep(sleep_time)
        # #boost lec
        # device.shell('input touchscreen tap 110 1480')
        # time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIA soft
        device.shell('input touchscreen tap 820 1571')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(15)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 204
    elif state == 204 and wet == 0 and "LAP 6" in extracted_text and (is_raining or "rain" in extracted_text or (time.time() - last_rain_change_time) < 60):
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
        state = 205
        wet = 1

    # elif state == 203 and wet == 1 and "LAP 6" in extracted_text and "Rain" not in extracted_text:
    #     #lec pitstop
    #     time.sleep(5)
    #     device.shell('input touchscreen tap 820 2265')
    #     time.sleep(2)
    #     #lecsofts
    #     device.shell('input touchscreen tap 820 1565')
    #     time.sleep(sleep_time)
    #     #lecserv
    #     device.shell('input touchscreen tap 836 1856')
    #     time.sleep(5)
    #     #boost lec
    #     device.shell('input touchscreen tap 1000 1480')
    #     time.sleep(sleep_time)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 216 2270')
    #     time.sleep(sleep_time)
    #     #2nddriversoft
    #     device.shell('input touchscreen tap 230 1565')
    #     time.sleep(sleep_time)
    #     #PIAserv
    #     device.shell('input touchscreen tap 290 1856')
    #     time.sleep(sleep_time)
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     state = 203
    #     wet = 0
    elif state == 204 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and "Rain" not in extracted_text:
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #boost lec
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        # time.sleep(5)
        # device.shell('input touchscreen tap 120 1630')
        # device.shell('input touchscreen tap 110 1630')

        state = 204
        
    elif state == 204 and "8/8" in extracted_text:
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 204

    #     #Barcelona one stopsoftspit
    # elif state == 201 and ("1/8" in extracted_text or "LAP1" in extracted_text or "LAP 1" in extracted_text):
    #     time.sleep(sleep_time)
    #     #tap lec
    #     device.shell('input touchscreen tap 220 2090')
    #     time.sleep(sleep_time)
    #     device.shell('input touchscreen tap 110 1480')
    #     time.sleep(sleep_time)
    #     device.shell('input touchscreen tap 1000 1480')
    #     # time.sleep(10)
    #     # device.shell('input touchscreen tap 120 1630')
    #     # time.sleep(13)
    #     # device.shell('input touchscreen tap 990 1630')
    #     print("success")
    #     state = 202

    # elif state == 202 and "LAP 4" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text):
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
    #     #lec pitstop
    #     time.sleep(5)
    #     device.shell('input touchscreen tap 820 2265')
    #     #lec wets
    #     time.sleep(2)
    #     device.shell('input touchscreen tap 830 2146')
    #     time.sleep(1.5)
    #     #lecserv
    #     device.shell('input touchscreen tap 836 1856')
    #     time.sleep(4)
    #     time.sleep(10)
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     time.sleep(sleep_time)
    #     #boost lec
    #     device.shell('input touchscreen tap 1000 1480')
    #     state = 203
    #     wet = 1

    # # elif state == 202 and ("LAP 4" in extracted_text or "LAP4" in extracted_text):
    # #     time.sleep(sleep_time)
    # #     #PIA pitstop
    # #     device.shell('input touchscreen tap 216 2270')
    # #     time.sleep(sleep_time)
    # #     #PIA med
    # #     device.shell('input touchscreen tap 302 1771')
    # #     time.sleep(sleep_time)
    # #     #PIAserv
    # #     device.shell('input touchscreen tap 290 1856')
    # #     time.sleep(sleep_time)
    # #     #boost pia
    # #     device.shell('input touchscreen tap 110 1480')
    # #     #lec pitstop
    # #     time.sleep(sleep_time)
    # #     device.shell('input touchscreen tap 820 2265')
    # #     time.sleep(sleep_time)
    # #     #lechard
    # #     device.shell('input touchscreen tap 852 1970')
    # #     time.sleep(sleep_time)
    # #     #lecserv
    # #     device.shell('input touchscreen tap 836 1856')
    # #     time.sleep(sleep_time)
    # #     #boost lec
    # #     device.shell('input touchscreen tap 1000 1480')
    # #     time.sleep(sleep_time)
    # #     state = 203
    # #     wet = 0

    # elif state == 202 and ("LAP 4" in extracted_text or "LAP4" in extracted_text):
    #     time.sleep(sleep_time)
    #     #lec pitstop
    #     time.sleep(sleep_time)
    #     device.shell('input touchscreen tap 820 2265')
    #     time.sleep(sleep_time)
    #     #lecmedium
    #     device.shell('input touchscreen tap 852 1770')
    #     time.sleep(sleep_time)
    #     #lecserv
    #     device.shell('input touchscreen tap 836 1856')
    #     time.sleep(sleep_time)
    #     #boost lec
    #     device.shell('input touchscreen tap 1000 1480')
    #     time.sleep(sleep_time)
    #     state = 203
    #     wet = 0

    # elif state == 203 and ("LAP 5" in extracted_text or "LAP5" in extracted_text):
    #     time.sleep(sleep_time)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 216 2270')
    #     time.sleep(sleep_time)
    #     #PIA hard
    #     device.shell('input touchscreen tap 302 1571')
    #     time.sleep(sleep_time)
    #     #PIAserv
    #     device.shell('input touchscreen tap 290 1856')
    #     time.sleep(10)
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     state = 203.5
    #     wet = 0

    # elif state == 203.5 and wet == 0 and "LAP 6" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text):
    #     time.sleep(sleep_time)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 216 2270')
    #     time.sleep(sleep_time)
    #     #pia wets
    #     device.shell('input touchscreen tap 300 2122')
    #     time.sleep(sleep_time)
    #     #PIAserv
    #     device.shell('input touchscreen tap 290 1856')
    #     time.sleep(sleep_time)
    #     #lec pitstop
    #     time.sleep(5)
    #     device.shell('input touchscreen tap 820 2265')
    #     #lec wets
    #     time.sleep(2)
    #     device.shell('input touchscreen tap 830 2146')
    #     time.sleep(sleep_time)
    #     #lecserv
    #     device.shell('input touchscreen tap 836 1856')
    #     time.sleep(15)
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     time.sleep(sleep_time)
    #     #boost lec
    #     device.shell('input touchscreen tap 1000 1480')
    #     state = 204
    #     wet = 1
    # elif state == 203 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and "Rain" not in extracted_text:
    #     time.sleep(sleep_time)
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     #boost lec
    #     time.sleep(0.5)
    #     device.shell('input touchscreen tap 1000 1480')
    #     time.sleep(5)
    #     # device.shell('input touchscreen tap 120 1630')
    #     device.shell('input touchscreen tap 110 1630')

    #     state = 203
        
    # elif state == 203 and "8/8" in extracted_text:
    #     time.sleep(sleep_time)
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     time.sleep(sleep_time)
    #     #boost lec
    #     device.shell('input touchscreen tap 1000 1480')
    #     state = 203

    #JEDDAH
    elif state == 151 and ("1/7" in extracted_text or "LAP1" in extracted_text or "LAP 1" in extracted_text or "/7" in extracted_text):
        time.sleep(boost_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(5)
        device.shell('input touchscreen tap 990 1630')
        time.sleep(5)
        device.shell('input touchscreen tap 120 1630')
        
        print("success")
        state = 152
        print(state)

    elif state == 152 and "LAP 2" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text):
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 216 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 300 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)
        #boost lec
        # device.shell('input touchscreen tap 110 1480')
        state = 153
        wet = 1

    elif state == 152 and "LAP 2" in extracted_text and "LAP1" not in extracted_text and "LAP 1" not in extracted_text and "Rain" not in extracted_text:
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIA soft
        device.shell('input touchscreen tap 300 1560')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(25)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 153

    elif state == 153 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and (is_raining or "rain" in extracted_text or (time.time() - last_rain_change_time) < 60):
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 820 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        time.sleep(25)
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 154
        wet = 1

    elif state == 153 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "Rain" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsoft
        device.shell('input touchscreen tap 820 1571')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(25)
        #boost lec
        # device.shell('input touchscreen tap 1000 1480')
        state = 154

    elif state == 154 and "LAP 4" in extracted_text and (is_raining or "rain" in extracted_text or (time.time() - last_rain_change_time) < 60):
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 216 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 300 2146')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        state = 155
        wet = 1

    elif state == 154 and "LAP 4" in extracted_text and "Rain" not in extracted_text and "LAP 3" not in extracted_text and "LAP 3" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIA med
        device.shell('input touchscreen tap 300 1560')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(25)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        print(time.time() - last_rain_change_time)
        state = 155

    elif state == 155 and ("LAP 5" in extracted_text or "LAP5" in extracted_text or "LAPS" in extracted_text) and (is_raining or "rain" in extracted_text or (time.time() - last_rain_change_time) < 60) and "Cloudy" not in extracted_text:
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 820 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        time.sleep(15)
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 156
        wet = 1

    elif state == 155 and ("LAP 5" in extracted_text or "LAP5" in extracted_text or "LAPS" in extracted_text) and "Rain" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(sleep_time)
        #lecsoft
        device.shell('input touchscreen tap 820 1771')
        time.sleep(sleep_time)
        # #lecserv
        device.shell('input touchscreen tap 836 2050')
        time.sleep(25)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 156

    elif state == 156 and ("LAP 6" in extracted_text or "LAP6" in extracted_text) and "Rain" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecsoft
        device.shell('input touchscreen tap 230 1571')
        time.sleep(sleep_time)
        # #lecserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(25)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        state = 157

    elif state == 157 and "7/7" in extracted_text:
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        state = 157

    #spielberg
    elif state == 10 and ("1/10" in extracted_text or "/10" in extracted_text):
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
        state = 13
        wet = 1

    elif state == 11 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecsofts
        device.shell('input touchscreen tap 230 1565')
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
        #PIAsoft
        device.shell('input touchscreen tap 820 1569')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost pia
        # device.shell('input touchscreen tap 1000 1480')
        state = 12
        wet = 0

    elif state == 12 and wet == 0 and ("LAP 7" in extracted_text or "LAP7" in extracted_text or "LAP?" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
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
        state = 13
        wet = 1

    elif state == 12 and ("LAP 7" in extracted_text or "LAP7" in extracted_text or "LAP?" in extracted_text) and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecsofts
        device.shell('input touchscreen tap 230 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(3)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIAsoft
        device.shell('input touchscreen tap 820 1569')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 2050')
        time.sleep(sleep_time)
        #boost pia
        # device.shell('input touchscreen tap 1000 1480')
        state = 13
        wet = 0

    # elif state == 12 and ("LAP 8" in extracted_text or "LAP8" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
    #     time.sleep(5)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 820 2270')
    #     time.sleep(sleep_time)
    #     #pia wets
    #     device.shell('input touchscreen tap 820 2122')
    #     time.sleep(sleep_time)
    #     #PIAserv
    #     device.shell('input touchscreen tap 836 1856')
    #     time.sleep(sleep_time)        
    #     #boost pia
    #     device.shell('input touchscreen tap 1000 1480')
    #     state = 14
    #     wet = 1

    elif wet == 1 and state == 13 and ("LAP 9" in extracted_text or "LAP9" in extracted_text) and "Rain" not in extracted_text and "Cloudy" in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 230 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 2050')
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
        device.shell('input touchscreen tap 836 2050')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 14
        wet = 0
    elif (state == 13 or state == 14) and "10/10" in extracted_text:
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
        time.sleep(5)
        # device.shell('input touchscreen tap 990 1630')
        time.sleep(7)
        # device.shell('input touchscreen tap 120 1630')
        time.sleep(10)
        # device.shell('input touchscreen tap 950 795')
        
        print("success")
        state = 22
        print(state)
    elif state == 22 and ("LAP 2" in extracted_text or "LAP2" in extracted_text) and "Rain" not in extracted_text and "Light" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60 and "Attack" not in extracted_text and "LAP1" not in extracted_text and "LAP 1" not in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 302 1571')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(5)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 23

    elif state == 23 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and (is_raining or "rain" in extracted_text or (time.time() - last_rain_change_time) < 60):
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
        state = 24
        wet = 1
    elif state == 23 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "Rain" not in extracted_text and "Light" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60 and "LAP 2" not in extracted_text and "LAP2" not in extracted_text and "Attack" not in extracted_text:

        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIA med
        device.shell('input touchscreen tap 852 1760')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        time.sleep(15)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 24
        wet = 0

    elif state == 24 and wet == 0 and "LAP 4" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text):
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
        state = 25
        wet = 1

    elif state == 24 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and "Rain" not in extracted_text and "Light" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 302 1571')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(5)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 25

    # elif state == 23 and ("LAP 5" in extracted_text or "LAP5" in extracted_text) and "Rain" not in extracted_text and "Light" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60 and "LAP 4" not in extracted_text and "LAP4" not in extracted_text and "Attack" not in extracted_text:
    #     time.sleep(sleep_time)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 216 2270')
    #     time.sleep(sleep_time)
    #     #PIAmed
    #     device.shell('input touchscreen tap 230 1565')
    #     time.sleep(sleep_time)
    #     # #PIAserv
    #     device.shell('input touchscreen tap 290 2050')
    #     time.sleep(5)
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
    #     wet = 0
    #     last_rain_change_time = time.time()

    elif (state == 24 or state == 25) and "6/6" in extracted_text and "Rain" not in extracted_text:
        time.sleep(boost_time)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        # device.shell('input touchscreen tap 1000 1480')
        # state = 24

    elif (state == 24 or state == 25) and "6/6" in extracted_text and "Rain" in extracted_text:
        # time.sleep(10)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        # time.sleep(sleep_time)
        #boost LEC
        # device.shell('input touchscreen tap 1000 1480')
        # state = 24
        
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

    elif state == 32 and wet == 0 and ("LAP 3" in extracted_text or "LAP3" in extracted_text):
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecmed
        device.shell('input touchscreen tap 302 1771')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(3)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        state = 33

    elif state == 33 and "LAP 4" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text):
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
        state = 34
        wet = 1

    elif state == 33 and ("LAP 4" in extracted_text or "LAP4" in extracted_text):
        # #lec pitstop
        # time.sleep(sleep_time)
        # device.shell('input touchscreen tap 216 2265')
        # time.sleep(sleep_time)
        # #lecsoft
        # device.shell('input touchscreen tap 302 1571')
        # time.sleep(sleep_time)
        # #lecserv
        # device.shell('input touchscreen tap 290 1856')
        # time.sleep(3)
        # #boost lec
        # device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 820 2270')
        time.sleep(sleep_time)
        #PIA soft
        device.shell('input touchscreen tap 852 1560')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 34
        wet = 0

    elif state == 34 and wet == 0 and "LAP5" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text):
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
        state = 35
        wet = 1

    # elif state == 33 and wet == 1 and "LAP5" in extracted_text and "Rain" in extracted_text:
    #     state = 34
    
    elif state == 34 and wet == 1 and "LAP5" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 230 1565')
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
        state = 35
        wet = 0
    
    elif state == 34 and "7/7" in extracted_text:
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
    elif state == 35 and "7/7" in extracted_text:
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
        #lecsofts
        device.shell('input touchscreen tap 230 1565')
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
        #PIAsoft
        device.shell('input touchscreen tap 820 1569')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost pia
        # device.shell('input touchscreen tap 1000 1480')
        state = 63
        wet = 0

    elif state == 63 and ("LAP 6" in extracted_text or "LAP6" in extracted_text) and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 230 1565')
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
        #PIAsoft
        device.shell('input touchscreen tap 820 1569')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(15)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 64
        wet = 0

    elif state == 64 and "LAP 8" in extracted_text and ("Rain" in extracted_text or "rain" in extracted_text):
        time.sleep(5)
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
        time.sleep(5)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #lec pitstop
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(6)
        #stop pia boost
        device.shell('input touchscreen tap 110 1630')
        state = 73
        wet = 1
        
    elif state == 73 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
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
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(2)
        #stop pia boost
        device.shell('input touchscreen tap 110 1630')
       
        state = 74
        wet = 1
    elif state == 72 and ("LAP 2" in extracted_text or "LAP2" in extracted_text):
        time.sleep(5)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIA soft
        device.shell('input touchscreen tap 230 1560')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 73
        wet = 0

    elif state == 73 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 820 1771')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 74
        wet = 0

    elif state == 74 and wet == 1 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
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
        # time.sleep(sleep_time)
        # #PIA pitstop
        # device.shell('input touchscreen tap 216 2270')
        # time.sleep(1.5)
        # #pia wets
        # device.shell('input touchscreen tap 300 2122')
        # time.sleep(1.5)
        # #PIAserv
        # device.shell('input touchscreen tap 290 1856')
        # time.sleep(sleep_time)        
        # #boost pia
        # device.shell('input touchscreen tap 110 1480')
        
        state = 75
        wet = 1

    elif state == 74 and wet == 0 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
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
        
        state = 75
        wet = 1

    elif state == 74 and ("LAP 4" in extracted_text or "LAP4" in extracted_text):
        time.sleep(sleep_time)
        #stop lec boost
        device.shell('input touchscreen tap 110 1630')
        time.sleep(5)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(sleep_time)
        #PIA soft
        device.shell('input touchscreen tap 230 1560')
        time.sleep(sleep_time)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        #lec pitstop
        time.sleep(30)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        # time.sleep(sleep_time)
        # device.shell('input touchscreen tap 820 2265')
        # time.sleep(2)
        # #lecsofts
        # device.shell('input touchscreen tap 820 1565')
        # time.sleep(1.5)
        # #lecserv
        # device.shell('input touchscreen tap 836 2050')
        time.sleep(sleep_time)
        time.sleep(2)
        
        state = 75
        wet = 0

    elif state == 75 and "6/6" in extracted_text:
        time.sleep(boost_time)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        

    elif state == 74 and "Rain" in extracted_text and "LAP 6" in extracted_text:
        # #boost LEC
        # device.shell('input touchscreen tap 1000 1480')
        time.sleep(boost_time)
        #boost PIA
        device.shell('input touchscreen tap 1000 1480')
        state = 1000
    #Abu Dhabi
    elif state == 81 and ("1/8" in extracted_text or "/8" in extracted_text):
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
    elif state == 82 and "LAP 3" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
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

    elif state == 82 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "/8" in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecsofts
        device.shell('input touchscreen tap 230 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
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
        #PIAserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(15)
        device.shell('input touchscreen tap 120 1630')
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 990 1630')
        state = 83
        wet = 0

    elif state == 83 and wet == 0 and "LAP 4" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
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
    #raining but previously car not fitted with wets
    elif state == 83 and wet == 0 and "LAP5" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
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
    

    elif state == 83 and wet == 0 and "LAP5" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        
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

    elif state == 83 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and "/8" in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecsofts
        device.shell('input touchscreen tap 230 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(2)
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
        device.shell('input touchscreen tap 836 2050')
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 1000 1480')
        state = 84
        wet = 0
    
    elif state == 83 and wet == 1 and "LAP 6" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
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

    elif state == 83 and wet == 0 and "LAP 6" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
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

    

    elif state == 83 and wet == 1 and "LAP 6" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 230 1565')
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
        state = 84
            
    elif state == 84 and "8/8" in extracted_text and "/8" in extracted_text:
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 84

    #Australia
    elif state == 110 and ("1/8" in extracted_text or "LAP1" in extracted_text or "LAP 1" in extracted_text or "/8" in extracted_text):
        time.sleep(sleep_time)
        #tap lec
        device.shell('input touchscreen tap 220 2090')
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        device.shell('input touchscreen tap 1000 1480')
        #lec boost again
        time.sleep(20)
        # device.shell('input touchscreen tap 110 1480')
        time.sleep(2)
        #stop lec boost
        device.shell('input touchscreen tap 110 1630')
        # time.sleep(13)
        # device.shell('input touchscreen tap 109 1618')
        # time.sleep(sleep_time)
        # device.shell('input touchscreen tap 110 1418')
        print("success")
        state = 111
    elif state == 111 and wet == 0 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
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
        lecwet = 1
        state = 112
        wet = 1
        print('test lap 3')
    elif state == 111 and ("LAP 3" in extracted_text or "LAP3" in extracted_text) and "Rain" not in extracted_text and "LAP2" not in extracted_text and "LAP 2" not in extracted_text and "Attack" not in extracted_text:
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecsoft
        device.shell('input touchscreen tap 230 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(sleep_time)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        # time.sleep(sleep_time)
        # #PIA pitstop
        # device.shell('input touchscreen tap 216 2270')
        # time.sleep(sleep_time)
        # #PIAmed
        # device.shell('input touchscreen tap 230 1769')
        # time.sleep(sleep_time)
        # #PIAserv
        # device.shell('input touchscreen tap 290 1856')
        # time.sleep(sleep_time)
        # #boost pia
        # device.shell('input touchscreen tap 110 1480')
        state = 112
        wet = 0

    elif state == 111 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
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
        state = 113

    elif state == 112 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
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
        state = 113

    elif state == 112 and ("LAP 4" in extracted_text or "LAP4" in extracted_text) and "Rain" not in extracted_text:
        # #lec pitstop
        # time.sleep(2)
        # device.shell('input touchscreen tap 820 2265')
        # time.sleep(sleep_time)
        # #lechards
        # device.shell('input touchscreen tap 820 1965')
        # time.sleep(sleep_time)
        # #lecserv
        # device.shell('input touchscreen tap 836 1856')
        # time.sleep(sleep_time)
        # #boost lec
        # device.shell('input touchscreen tap 1000 1480')
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
        state = 113
        wet = 0

    elif state == 113 and wet == 0 and ("LAP5" in extracted_text or "LAP 5" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        # time.sleep(sleep_time)
        # #PIA pitstop
        # device.shell('input touchscreen tap 216 2270')
        # time.sleep(sleep_time)
        # #pia wets
        # device.shell('input touchscreen tap 300 2122')
        # time.sleep(sleep_time)
        # #PIAserv
        # device.shell('input touchscreen tap 290 1856')
        # time.sleep(sleep_time)        
        # #boost pia
        # device.shell('input touchscreen tap 110 1480')
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
        state = 114
        print("lol")

    elif state == 113 and ("LAP 6" in extracted_text or "LAP6" in extracted_text) and "/8" in extracted_text and "Rain" not in extracted_text and "LAP4" not in extracted_text and "LAP 4" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 216 2265')
        time.sleep(sleep_time)
        #lecsoft
        device.shell('input touchscreen tap 230 1565')
        time.sleep(sleep_time)
        #lecserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(25)
        #boost lec
        device.shell('input touchscreen tap 110 1480')
        time.sleep(sleep_time)
        # #PIA pitstop
        # device.shell('input touchscreen tap 216 2270')
        # time.sleep(sleep_time)
        # #PIAhards
        # device.shell('input touchscreen tap 230 1969')
        # time.sleep(sleep_time)
        # #PIAserv
        # device.shell('input touchscreen tap 290 1856')
        # time.sleep(sleep_time)
        # #boost pia
        # device.shell('input touchscreen tap 110 1480')
        state = 114
        wet = 0
    #raining but previously car not fitted with wets
    elif state == 114 and wet == 0 and ("LAP7" in extracted_text or "LAP 7" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
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
        state = 115
        print("lol")
    

    # elif state == 114 and wet == 1 and ("LAP7" in extracted_text or "LAP 7" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
        
    #     # time.sleep(sleep_time)
    #     # #PIA pitstop
    #     # device.shell('input touchscreen tap 216 2270')
    #     # time.sleep(sleep_time)
    #     # #pia wets
    #     # device.shell('input touchscreen tap 300 2122')
    #     # time.sleep(sleep_time)
    #     # #PIAserv
    #     # device.shell('input touchscreen tap 290 1856')
    #     # time.sleep(sleep_time)        
    #     # #boost pia
    #     # device.shell('input touchscreen tap 110 1480')
    #     #lec pitstop
    #     time.sleep(sleep_time)
    #     device.shell('input touchscreen tap 820 2265')
    #     #lec wets
    #     time.sleep(sleep_time)
    #     device.shell('input touchscreen tap 830 2146')
    #     time.sleep(sleep_time)
    #     #lecserv
    #     device.shell('input touchscreen tap 836 1856')
    #     time.sleep(sleep_time)
    #     #boost lec
    #     device.shell('input touchscreen tap 1000 1480')
    #     state = 115
    #     wet = 1
    #     print("lol")
    
    # elif state == 112 and wet == 1 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text):
    #     time.sleep(sleep_time)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 216 2270')
    #     time.sleep(sleep_time)
    #     #pia wets
    #     device.shell('input touchscreen tap 300 2122')
    #     time.sleep(sleep_time)
    #     #PIAserv
    #     device.shell('input touchscreen tap 290 1856')
    #     time.sleep(8)        
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     # #lec pitstop
    #     # time.sleep(sleep_time)
    #     # device.shell('input touchscreen tap 820 2265')
    #     # #lec wets
    #     # time.sleep(2)
    #     # device.shell('input touchscreen tap 830 2146')
    #     # time.sleep(sleep_time)
    #     # #lecserv
    #     # device.shell('input touchscreen tap 836 1856')
    #     # time.sleep(3)
    #     # #boost lec
    #     # device.shell('input touchscreen tap 1000 1480')
    #     state = 115
    #     wet = 1

    elif state == 114 and wet == 0 and ("LAP7" in extracted_text or "LAP 7" in extracted_text) and ("Rain" in extracted_text or "rain" in extracted_text) and "/8" in extracted_text:
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
        state = 115
        wet = 1

    

    elif state == 114 and wet == 1 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and "Rain" not in extracted_text and "Light" not in extracted_text and not is_raining and (time.time() - last_rain_change_time) > 60:
        time.sleep(sleep_time)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIAmed
        device.shell('input touchscreen tap 230 1569')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 2050')
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
        device.shell('input touchscreen tap 836 2050')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 115
        wet = 0

    elif state == 114 and ("LAP6" in extracted_text or "LAP 6" in extracted_text) and "Rain" not in extracted_text and "/8" in extracted_text:
        time.sleep(sleep_time)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #boost lec
        time.sleep(sleep_time)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(sleep_time)
        # device.shell('input touchscreen tap 120 1630')
        # device.shell('input touchscreen tap 110 1630')
        
        state == 114
            
    elif (state == 115 or state == 114) and ("8/8" in extracted_text or "/8" in extracted_text):
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(boost_time)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')    

    elif "Debrief" in extracted_text or "WINNER" in extracted_text or "Activate now" in extracted_text or "Standard" in extracted_text:
        if (crateloc[0].size > 0 or winnerloc[0].size > 0):
            winner1 += 1
            race += 1
            print(f"won: {winner1}")
            print(f"races: {race}")
            elapsed_time_seconds = time.time() - start_time
            hours, remainder = divmod(elapsed_time_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"Playing for {int(hours)} hours and {int(minutes)} minutes.")
        else: 
            time.sleep(sleep_time)
            race += 1
            print(f"won: {winner1}")
            print(f"races: {race}")
            elapsed_time_seconds = time.time() - start_time
            hours, remainder = divmod(elapsed_time_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"Playing for {int(hours)} hours and {int(minutes)} minutes.")
        time.sleep(2)
        device.shell('input touchscreen tap 857 2250')
        time.sleep(4)
        device.shell('input touchscreen tap 580 2250')
        time.sleep(4)
        device.shell('input touchscreen tap 950 795')
        state = 100
        wet = 0
        lecwet = 0

    elif ("continue" in extracted_text or "POS. PLAYER Races TOTAL" in extracted_text):
        device.shell('input touchscreen tap 580 2250')
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
        time.sleep(sleep_time)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')

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
        

