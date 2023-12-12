from ppadb.client import Client
import subprocess
from PIL import Image 
import pytesseract
import time 
import numpy
import os
import cv2

os.environ["TESSDATA_PREFIX"] = 'C:/Users/seeho/testadb/Tesseract-OCR/tessdata'
adb = Client(host='127.0.0.1', port= 5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()



device = devices[0]

# Capture a screenshot and save it

state = 100
wet = 0
barca = 0
jeddah = 0
winner1 = 0
race = 0

# Check if the extracted text is "7"
while True:
    time.sleep(0.2)
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
    cloudres = cv2.matchTemplate(image, cloud, cv2.TM_CCOEFF_NORMED)
    lap8res = cv2.matchTemplate(image, lap8, cv2.TM_CCOEFF_NORMED)
    lap7res = cv2.matchTemplate(image, lap7, cv2.TM_CCOEFF_NORMED)
    lightrainres = cv2.matchTemplate(image, lightrain, cv2.TM_CCOEFF_NORMED)
    lap10res = cv2.matchTemplate(image, lap10, cv2.TM_CCOEFF_NORMED)
    winnerres = cv2.matchTemplate(image, winner, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9

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
    
    # # Perform OCR on the screenshot
    pytesseract.pytesseract.tesseract_cmd = 'C:/Users/seeho/testadb/Tesseract-OCR/tesseract.exe'
    
    extracted_text = pytesseract.image_to_string(image, lang='eng', config='--psm 6 tessedit_char_unblacklist=0123456789')
    #cv2.imwrite('output.png', image)
    # Print the extracted text

    # print(extracted_text)
    # print(lap8loc[0].size)
    print(state)
    # Clean up the screenshot file
    # os.remove('screen.png')
    if state == 100 and "REWARDS" in extracted_text:
        #race
        device.shell('input touchscreen tap 560 1607')
        print("race")
        time.sleep(2)
        #Duels
        device.shell('input touchscreen tap 551 540')
        time.sleep(2)
        print("duels")
        #slide right
        device.shell('input swipe 200 1300 600 1300 1000')
        time.sleep(0.5)
        device.shell('input swipe 200 1300 600 1300 1000')
        time.sleep(0.5)
        device.shell('input swipe 200 1300 600 1300 1000')
        time.sleep(1)
        device.shell('input touchscreen tap 580 1300')
        time.sleep(1.5)
        device.shell('input touchscreen tap 550 1485')
        state = 101

    elif state == 101 and "ZANDVOORT" in extracted_text:
        time.sleep(25)
        state = 30
        print("ZANDVOORT")

    elif state == 101 and "SINGAPORE" in extracted_text:
        time.sleep(25)
        state = 20
        print("SINGAPORE")

    elif state == 101 and "BELGIUM" in extracted_text:
        time.sleep(20)
        state = 70
        print("STAVELOT")

    elif state == 101 and "HUNGARY" in extracted_text:
        time.sleep(25)
        state = 200
        print("HUNGARY")
    
    elif state == 101 and "MEXICO CITY" in extracted_text:
        time.sleep(25)
        state = 200
        print("Mexico City")
            
    #num of laps race pg
    elif state == 101 and "BARCELONA" in extracted_text:
        time.sleep(25)
        state = 200
        print("BARCA")

    elif state == 101 and "MONTREAL" in extracted_text:
        time.sleep(25)
        state = 200
        print("MONTREAL")

    elif state == 101 and "MONACO" in extracted_text:
        time.sleep(25)
        state = 200
        print("MONACO")
    
    elif state == 101 and "JEDDAH" in extracted_text:
        time.sleep(25)
        state = 150
        print("JEDDAH")
    
    elif state == 101 and "BRAZIL" in extracted_text:
        time.sleep(20)
        state = 60
        print("SAO PAULO")

    elif cloudloc[0].size > 0 and state == 80:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 81

    elif cloudloc[0].size == 0 and state == 80:
        print("lap8")
        #lecmedium
        device.shell('input touchscreen tap 900 1156')
        time.sleep(1)
        #PIA Hards
        device.shell('input touchscreen tap 300 1156')
        time.sleep(1)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 81

    elif cloudloc[0].size > 0 and state == 60:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 61

    elif cloudloc[0].size == 0 and state == 60:
        print("lap8")
        #lecmedium
        device.shell('input touchscreen tap 900 1156')
        time.sleep(1)
        #PIA Hards
        device.shell('input touchscreen tap 300 1156')
        time.sleep(1)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 61

    elif cloudloc[0].size > 0 and state == 70:
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 71

    elif cloudloc[0].size == 0 and state == 70:
        print("lap8")
        #lecmedium
        device.shell('input touchscreen tap 900 1156')
        time.sleep(1)
        #PIA Hards
        device.shell('input touchscreen tap 300 1156')
        time.sleep(1)
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
        device.shell('input touchscreen tap 900 1156')
        time.sleep(1)
        #PIA Hards
        device.shell('input touchscreen tap 300 1156')
        time.sleep(1)
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
        device.shell('input touchscreen tap 900 1156')
        time.sleep(1)
        #PIA Hards
        device.shell('input touchscreen tap 300 1156')
        time.sleep(1)
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
        device.shell('input touchscreen tap 900 1156')
        time.sleep(1)
        #PIA Hards
        device.shell('input touchscreen tap 300 1156')
        time.sleep(1)
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
        device.shell('input touchscreen tap 900 1156')
        time.sleep(1)
        #PIA Hards
        device.shell('input touchscreen tap 300 1156')
        time.sleep(1)
        #start race
        device.shell('input touchscreen tap 588 2250')
        state = 201

    elif state == 101 and lap10loc[0].size > 0:
        if cloudloc[0].size > 0:
            time.sleep(2)
            device.shell('input touchscreen tap 588 2250')
            state = 10
            wet = 1
        else:
            #lecmedium
            time.sleep(2)
            device.shell('input touchscreen tap 900 1156')
            time.sleep(1)
            #PIA hards
            device.shell('input touchscreen tap 300 1350')
            time.sleep(1)
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
            device.shell('input touchscreen tap 900 1156')
            time.sleep(1)
            #PIA hards
            device.shell('input touchscreen tap 300 1350')
            time.sleep(1)
            #start race
            device.shell('input touchscreen tap 588 2250')
            state = 0
            barca = 1
            
    #check for num of laps and rain
    elif state == 101 and lap7loc[0].size > 0:
        if cloudloc[0].size > 0:
            #start race
            device.shell('input touchscreen tap 588 2250')
            wet = 1
            state = 0
        else:
            print("lap7")
            #lecmedium
            device.shell('input touchscreen tap 900 1156')
            time.sleep(1)
            #PIA hards
            device.shell('input touchscreen tap 300 1350')
            time.sleep(1)
            #start race
            device.shell('input touchscreen tap 588 2250')
            time.sleep(4)
            state = 0
            jeddah = 1

    elif state == 0 and "1/7" in extracted_text:
        time.sleep(1)
        #tap lec
        device.shell('input touchscreen tap 820 2090')
        time.sleep(1)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        device.shell('input touchscreen tap 110 1480')
        # time.sleep(15)
        # device.shell('input touchscreen tap 120 1630')
        # time.sleep(8)
        # device.shell('input touchscreen tap 990 1630')
        
        print("success")
        state = 0.1
        print(state)

    elif state == 0.1 and "LAP 3" in extracted_text and "Rain" in extracted_text and "/7" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(1)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.2
        wet = 1

    elif state == 0.1 and wet == 0 and "LAP 4" in extracted_text and "Rain" in extracted_text and "/7" in extracted_text:
        #lec pitstop
        time.sleep(8)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(4)
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.2
        wet = 1

    elif state == 0.1 and "LAP 3" in extracted_text and "/7" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(1)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #PIAmed
        device.shell('input touchscreen tap 230 1769')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(5)
        #lecboost
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(5)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.2
        wet = 0
    elif state == 0.2 and "LAP5" in extracted_text and "Rain" in extracted_text and "/7" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(1)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        time.sleep(20)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.3
        wet = 1
    elif state == 0.2 and "LAP5" in extracted_text  and "/7" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(1)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 2050')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #PIAmed
        device.shell('input touchscreen tap 230 1769')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(5)
        state = 0.3

    elif state == 0.2 and wet == 0 and "LAP 6" in extracted_text and "Rain" in extracted_text and "/7" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(1)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 0.2
        wet = 1

    elif state == 0.3 and "LAP 7" in extracted_text and "/7" in extracted_text:
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 1000


    elif state == 0 and "1/8" in extracted_text:
        time.sleep(1)
        #tap lec
        device.shell('input touchscreen tap 820 2090')
        time.sleep(1)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        device.shell('input touchscreen tap 110 1480')
        # time.sleep(13)
        # device.shell('input touchscreen tap 109 1618')
        # time.sleep(1)
        # device.shell('input touchscreen tap 110 1418')
        print("success")
        state = 1
    elif state == 1 and "LAP 3" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        
        #lec pitstop
        time.sleep(5)
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
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')

        state = 2
        wet = 1
        print('test lap 3')

    elif state == 1 and "LAP 3" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIAmed
        device.shell('input touchscreen tap 230 1769')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 2
        wet = 0

    elif state == 2 and wet == 0 and "LAP 4" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(2)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 3
        wet = 1
    #raining but previously car not fitted with wets
    elif state == 2 and wet == 0 and "LAP5" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')

        state = 3
        print("lol")
    

    elif state == 2 and wet == 0 and "LAP5" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        
        #lec pitstop
        time.sleep(5)
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
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')

        state = 3
        print("lol")

    elif state == 2 and "LAP5" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 852 1771')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #2nddrivermedium
        device.shell('input touchscreen tap 302 1771')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 3

    # elif state == 2 and "LAPS" in extracted_text and "/8" in extracted_text:
    #     #lec pitstop
    #     time.sleep(5)
    #     device.shell('input touchscreen tap 820 2265')
    #     time.sleep(2)
    #     #lecmedium
    #     device.shell('input touchscreen tap 852 1771')
    #     time.sleep(1.5)
    #     #lecserv
    #     device.shell('input touchscreen tap 836 1856')
    #     time.sleep(5)
    #     #boost lec
    #     device.shell('input touchscreen tap 1000 1480')
    #     time.sleep(1)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 216 2270')
    #     time.sleep(1.5)
    #     #2nddrivermedium
    #     device.shell('input touchscreen tap 302 1771')
    #     time.sleep(1.5)
    #     #PIAserv
    #     device.shell('input touchscreen tap 290 1856')
    #     time.sleep(1)
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     state = 3

    
    elif state == 2 and wet == 1 and "LAP 6" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(5)
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
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 3

    elif state == 2 and wet == 0 and "LAP 6" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(5)
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
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 3

    

    elif state == 2 and wet == 1 and "LAP 6" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(8)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIAmed
        device.shell('input touchscreen tap 230 1769')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 3
            
    elif state == 3 and "LAP8" in extracted_text and "/8" in extracted_text:
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 1000
    
    #Barcelona one stop
    elif state == 201 and "1/8" in extracted_text:
        time.sleep(1)
        #tap lec
        device.shell('input touchscreen tap 820 2090')
        time.sleep(1)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        device.shell('input touchscreen tap 110 1480')
        # time.sleep(10)
        # device.shell('input touchscreen tap 120 1630')
        # time.sleep(8)
        # device.shell('input touchscreen tap 990 1630')
        print("success")
        state = 202

    elif state == 202 and "LAP 4" in extracted_text and "Rain" in extracted_text:
        #lec pitstop
        time.sleep(8)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(4)
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 203
        wet = 1

    elif state == 202 and "LAP 4" in extracted_text:
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(1)
        #lecmedium
        device.shell('input touchscreen tap 852 1771')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(1)
        
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #2nddrivermedium
        device.shell('input touchscreen tap 302 1771')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 203

    elif state == 203 and wet == 0 and "LAP 6" in extracted_text and "Rain" in extracted_text:
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
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 203
        wet = 1

    elif state == 203 and wet == 1 and "LAP 6" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #PIAmed
        device.shell('input touchscreen tap 230 1769')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 204
        wet = 0
        
    elif state == 203 and "LAP 8" in extracted_text:
        time.sleep(1)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 203

    #JEDDAH
    elif state == 151 and "1/7" in extracted_text:
        time.sleep(1.5)
        #tap lec
        device.shell('input touchscreen tap 820 2090')
        time.sleep(1)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        device.shell('input touchscreen tap 110 1480')
        # time.sleep(10)
        # device.shell('input touchscreen tap 120 1630')
        # time.sleep(10)
        # device.shell('input touchscreen tap 990 1630')
        
        print("success")
        state = 152
        print(state)
    elif state == 152 and "LAP 2" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 852 1771')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIA medium
        device.shell('input touchscreen tap 302 1771')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 153
    elif state == 153 and "LAP 4" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 852 1771')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #2nddrivermedium
        device.shell('input touchscreen tap 302 1771')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 154
    elif state == 154 and "LAP 6" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1.5)
        # #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIAmed
        device.shell('input touchscreen tap 230 1769')
        time.sleep(1.5)
        # #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 155

    elif state == 155 and "LAP 7" in extracted_text:
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        state = 155

    #spielberg
    elif state == 10 and "1/10" in extracted_text:
        time.sleep(1)
        #tap lec
        device.shell('input touchscreen tap 820 2090')
        time.sleep(1)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        device.shell('input touchscreen tap 110 1480')
        state = 11
    
    elif state == 11 and "LAP5" in extracted_text and "Rain" in extracted_text:
        time.sleep(5)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 12
        wet = 1


    elif state == 11 and "LAP 4" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(3)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #2ndriversoft
        device.shell('input touchscreen tap 230 1565')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 12
        wet = 0

    elif state == 12 and "LAP 7" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(1)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(3)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #2ndriversoft
        device.shell('input touchscreen tap 230 1565')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 13
        wet = 0

    # elif state == 12 and "LAP 8" in extracted_text and "Rain" in extracted_text:
    #     time.sleep(5)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 216 2270')
    #     time.sleep(1)
    #     #pia wets
    #     device.shell('input touchscreen tap 300 2122')
    #     time.sleep(1)
    #     #PIAserv
    #     device.shell('input touchscreen tap 290 1856')
    #     time.sleep(1)        
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     state = 13
    #     wet = 1

    elif wet == 1 and state == 13 and "LAP 9" in extracted_text and "Rain" not in extracted_text and "Partly Cloudy" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #2ndriversoft
        device.shell('input touchscreen tap 230 1565')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 13
        wet = 0
    elif state == 13 and "LAP 10" in extracted_text:
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        state = 13

    #Singapore
    elif state == 21 and "1/6" in extracted_text:
        time.sleep(1.5)
        #tap lec
        device.shell('input touchscreen tap 820 2090')
        time.sleep(1)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(15)
        device.shell('input touchscreen tap 120 1630')
        time.sleep(10)
        device.shell('input touchscreen tap 990 1630')
        
        print("success")
        state = 22
        print(state)
    elif state == 22 and "LAP 3" in extracted_text and "Rain" in extracted_text:
        time.sleep(5)
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        
        state = 23
        wet = 1
    elif state == 22 and "LAP 3" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 852 1771')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #2nddrivermedium
        device.shell('input touchscreen tap 302 1771')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 23
        wet = 0

    elif state == 23 and wet == 0 and "LAP 4" in extracted_text and "Rain" in extracted_text:
        time.sleep(5)
        #lec pitstop
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        
        state = 24
        wet = 1
    
    elif state == 23 and "LAP5" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(1)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        # #lecserv
        device.shell('input touchscreen tap 836 2050')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #PIAmed
        device.shell('input touchscreen tap 230 1565')
        time.sleep(1)
        # #PIAserv
        device.shell('input touchscreen tap 290 2050')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 24

    elif state == 23 and "LAP 6" in extracted_text:
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')

    elif state == 24 and "LAP 6" in extracted_text:
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')

    #ZANDVOORT
    elif state == 31 and "1/7" in extracted_text:
        time.sleep(0.5)
        #tap lec
        device.shell('input touchscreen tap 820 2090')
        time.sleep(1)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(15)
        device.shell('input touchscreen tap 120 1630')
        time.sleep(10)
        device.shell('input touchscreen tap 990 1630')
        
        print("success")
        state = 32

    elif state == 32 and "LAP 4" in extracted_text and "Rain" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(1)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        
        state = 33
        wet = 1

    elif state == 32 and "LAP 4" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 852 1771')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(2)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIA medium
        device.shell('input touchscreen tap 302 1771')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 33
        wet = 0

    elif state == 33 and wet == 0 and "LAP6" in extracted_text and "Rain" in extracted_text:
        time.sleep(5)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 34
        wet = 1

    elif state == 33 and wet == 1 and "LAP5" in extracted_text and "Rain" in extracted_text:
        state = 34
    
    elif state == 33 and wet == 1 and "LAP5" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #2nddriversofts
        device.shell('input touchscreen tap 230 1565')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 34
        wet = 0
    
    elif state == 33 and "LAP6" in extracted_text:
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
    elif state == 34 and "LAP6" in extracted_text:
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')

    #BRAZIL SAO PAULO
    elif state == 61 and "1/9" in extracted_text:
        time.sleep(1)
        #tap lec
        device.shell('input touchscreen tap 820 2090')
        time.sleep(1)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        device.shell('input touchscreen tap 110 1480')
        state = 62
    
    elif state == 62 and "LAP 4" in extracted_text and "Rain" in extracted_text:
        time.sleep(35)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 63
        wet = 1

    elif state == 62 and "LAP 4" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(3)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #2nddriversofts
        device.shell('input touchscreen tap 230 1565')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 63
        wet = 0

    elif state == 63 and "LAP 7" in extracted_text and "Rain" not in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(1)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(3)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #2nddriversofts
        device.shell('input touchscreen tap 230 1565')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 64
        wet = 0

    # elif state == 64 and "LAP 8" in extracted_text and "Rain" in extracted_text:
    #     time.sleep(5)
    #     #PIA pitstop
    #     device.shell('input touchscreen tap 216 2270')
    #     time.sleep(1)
    #     #pia wets
    #     device.shell('input touchscreen tap 300 2122')
    #     time.sleep(1)
    #     #PIAserv
    #     device.shell('input touchscreen tap 290 1856')
    #     time.sleep(1)        
    #     #boost pia
    #     device.shell('input touchscreen tap 110 1480')
    #     state = 65
    #     wet = 1
    elif state == 65 and "LAP 9" in extracted_text:
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        state = 1000
        
    elif state == 64 and "LAP 9" in extracted_text:
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')
        state = 1000

    #SPA
    elif state == 71 and "1/6" in extracted_text:
        time.sleep(1.5)
        #tap lec
        device.shell('input touchscreen tap 820 2090')
        time.sleep(1)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        device.shell('input touchscreen tap 110 1480')
        time.sleep(5)
        device.shell('input touchscreen tap 120 1630')
        time.sleep(3)
        device.shell('input touchscreen tap 990 1630')
        time.sleep(4)
        device.shell('input touchscreen tap 950 795')
        
        print("success")
        state = 72
        print(state)
    elif state == 72 and "LAP 2" in extracted_text and "Rain" in extracted_text:
        time.sleep(35)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(1)
        #lec pitstop
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        
       
        state = 73
        wet = 1
    elif state == 72 and "LAP 3" in extracted_text:
        time.sleep(5)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #PIA hard
        device.shell('input touchscreen tap 302 1960')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecmedium
        device.shell('input touchscreen tap 852 1771')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(1)
        time.sleep(10)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        state = 73
        wet = 0

    # elif state == 73 and "LAP 4" in extracted_text and "Rain" in extracted_text:
        # time.sleep(5)
        # #lec pitstop
        # device.shell('input touchscreen tap 820 2265')
        # #lec wets
        # time.sleep(2)
        # device.shell('input touchscreen tap 830 2146')
        # time.sleep(1)
        # #lecserv
        # device.shell('input touchscreen tap 836 1856')
        # time.sleep(5)
        # #boost lec
        # device.shell('input touchscreen tap 1000 1480')
        # time.sleep(1)
        # #PIA pitstop
        # device.shell('input touchscreen tap 216 2270')
        # time.sleep(1.5)
        # #pia wets
        # device.shell('input touchscreen tap 300 2122')
        # time.sleep(1.5)
        # #PIAserv
        # device.shell('input touchscreen tap 290 1856')
        # time.sleep(1)        
        # #boost pia
        # device.shell('input touchscreen tap 110 1480')
        
        # state = 74
        # wet = 1

    elif state == 73 and "LAP5" in extracted_text:
        time.sleep(1)
        #stop lec boost
        device.shell('input touchscreen tap 990 1630')
        time.sleep(5)
        #PIA pitstop
        device.shell('input touchscreen tap 216 1565')
        time.sleep(1.5)
        #PIA 
        device.shell('input touchscreen tap 302 2270')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 2050')
        
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        #lec pitstop
        time.sleep(1)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 2050')
        time.sleep(1)
        time.sleep(2)
        
        state = 74
        wet = 0

    elif state == 74 and "LAP 6" in extracted_text:
        time.sleep(1)
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')

    elif state == 74 and "Rain" in extracted_text and "LAP 6" in extracted_text:
        # #boost LEC
        # device.shell('input touchscreen tap 1000 1480')
        # time.sleep(1)
        # #boost PIA
        # device.shell('input touchscreen tap 110 1480')
        state = 1000

    #Abu Dhabi
    elif state == 81 and "1/8" in extracted_text:
        time.sleep(1)
        #tap lec
        device.shell('input touchscreen tap 820 2090')
        time.sleep(1)
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        device.shell('input touchscreen tap 110 1480')
        # time.sleep(13)
        # device.shell('input touchscreen tap 109 1618')
        # time.sleep(1)
        # device.shell('input touchscreen tap 110 1418')
        print("success")
        state = 82
    elif state == 82 and "LAP 3" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        
        #lec pitstop
        time.sleep(5)
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
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')

        state = 83
        wet = 1
        print('test lap 3')

    elif state == 82 and "LAP 3" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(5)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #2nddriversofts
        device.shell('input touchscreen tap 230 1565')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        time.sleep(15)
        device.shell('input touchscreen tap 990 1630')
        time.sleep(1)
        device.shell('input touchscreen tap 120 1630')
        state = 83
        wet = 0

    elif state == 83 and wet == 0 and "LAP 4" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(8)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1.5)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(4)
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        time.sleep(15)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 84
        wet = 1
    #raining but previously car not fitted with wets
    elif state == 83 and wet == 0 and "LAP5" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        
        #lec pitstop
        time.sleep(5)
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
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')

        state = 84
        print("lol")
    

    elif state == 83 and wet == 0 and "LAP5" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        
        #lec pitstop
        time.sleep(5)
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
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1.5)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1.5)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')

        state = 84
        print("lol")

    elif state == 83 and "LAP6" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #2nddriversofts
        device.shell('input touchscreen tap 230 1565')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 84
        wet = 0
    
    elif state == 83 and wet == 1 and "LAP 6" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 84

    elif state == 83 and wet == 0 and "LAP 6" in extracted_text and "Rain" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        #lec wets
        time.sleep(2)
        device.shell('input touchscreen tap 830 2146')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #pia wets
        device.shell('input touchscreen tap 300 2122')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)        
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 84

    

    elif state == 83 and wet == 1 and "LAP 6" in extracted_text and "/8" in extracted_text:
        #lec pitstop
        time.sleep(1)
        device.shell('input touchscreen tap 820 2265')
        time.sleep(2)
        #lecsofts
        device.shell('input touchscreen tap 820 1565')
        time.sleep(1)
        #lecserv
        device.shell('input touchscreen tap 836 1856')
        time.sleep(5)
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        #PIA pitstop
        device.shell('input touchscreen tap 216 2270')
        time.sleep(1)
        #2nddriversofts
        device.shell('input touchscreen tap 230 1565')
        time.sleep(1)
        #PIAserv
        device.shell('input touchscreen tap 290 1856')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 84
            
    elif state == 84 and "LAP 8" in extracted_text and "/8" in extracted_text:
        #boost lec
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost pia
        device.shell('input touchscreen tap 110 1480')
        state = 1000

    elif "WINNER" in extracted_text or "Debrief" in extracted_text:
        if winnerloc[0].size > 0:
            winner1 += 1
            race += 1
            print(winner1)
            print(race)
        else: 
            race += 1
            print(f"won: {winner1}")
            print(f"races: {race}")
        time.sleep(2)
        device.shell('input touchscreen tap 857 2250')
        time.sleep(5)
        device.shell('input touchscreen tap 580 2250')
        time.sleep(4)
        device.shell('input touchscreen tap 950 795')
        state = 100
        wet = 0
    elif "Standard Crate" in extracted_text:
        if winnerloc[0].size > 0:
            winner1 += 1
            race += 1
            print(winner1)
            print(race)
        else: 
            race += 1
            print(f"won: {winner1}")
            print(f"races: {race}")
        time.sleep(2)
        device.shell('input touchscreen tap 857 2250')
        time.sleep(5)
        device.shell('input touchscreen tap 580 2250')
        time.sleep(4)
        device.shell('input touchscreen tap 950 795')
        state = 100
        wet = 0

    elif "continue" in extracted_text:
        device.shell('input touchscreen tap 580 2250')

    elif "resume" in extracted_text:
        #boost LEC
        device.shell('input touchscreen tap 1000 1480')
        time.sleep(1)
        #boost PIA
        device.shell('input touchscreen tap 110 1480')


    
    
        




        
    

# print(extracted_text)

# device = devices[0]
# device.shell('input touchscreen swipe 500 500 500 1000 2000')

# image = device.screencap()

# with open('screen.png', 'wb') as f:
#     f.write(image)

# image = Image.open('screen.png')
# image = numpy.array(image, dtype=numpy.uint8)
# # Perform OCR on the screenshot
# extracted_text = pytesseract.image_to_string(image)

# # Print the extracted text
# print(extracted_text)

# # Clean up the screenshot file

