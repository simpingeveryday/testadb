from ppadb.client import Client
import subprocess
from PIL import Image 
import pytesseract
import time 
import numpy
import os
import cv2
#changes to jeddah and 7 laps races strat

os.environ["TESSDATA_PREFIX"] = 'C:/Users/seeho/testadb/misc/Tesseract-OCR/tessdata'
adb = Client(host='127.0.0.1', port= 5037)
devices = adb.devices()
start_time = time.time()
if len(devices) == 0:
    print('no device attached')
    quit()



device = devices[0]
reset = 0
# Capture a screenshot and save it

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
    cross = cv2.imread('cross1.jpg')
    cross2 = cv2.imread('cross2.jpg')
    cross3 = cv2.imread('cross3.jpg')
    leftcross = cv2.imread('leftcross.jpg')


    crossres = cv2.matchTemplate(image, cross, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_crossloc = cv2.minMaxLoc(crossres)
    top_leftcross = max_crossloc
    heightcross, widthcross, _ = cross.shape
    center_x1 = top_leftcross[0] + widthcross // 2
    center_y1 = top_leftcross[1] + heightcross // 2
    
    crossres2 = cv2.matchTemplate(image, cross2, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_cross2loc = cv2.minMaxLoc(crossres2)
    top_leftcross2 = max_cross2loc
    heightcross2, widthcross2, _ = cross2.shape
    center_x2 = top_leftcross2[0] + widthcross2 // 2
    center_y2 = top_leftcross2[1] + heightcross2 // 2

    crossres3 = cv2.matchTemplate(image, cross3, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_cross3loc = cv2.minMaxLoc(crossres3)
    top_leftcross3 = max_cross3loc
    heightcross3, widthcross3, _ = cross2.shape
    center_x3 = top_leftcross3[0] + widthcross3 // 2
    center_y3 = top_leftcross3[1] + heightcross3 // 2

    leftcrossres = cv2.matchTemplate(image, leftcross, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_leftcrossloc = cv2.minMaxLoc(leftcrossres)
    top_leftleftcross = max_leftcrossloc
    heightleftcross, widthleftcross, _ = leftcross.shape
    center_x4 = top_leftleftcross[0] + widthleftcross // 2
    center_y4 = top_leftleftcross[1] + heightleftcross // 2

    threshold = 0.9
    threshold2 = 0.58

    crossloc = numpy.where(crossres >= threshold)
    for pt in zip(*crossloc[::-1]):
        bottom_right = (pt[0] + cross.shape[1], pt[1] + cross.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    crossloc2 = numpy.where(crossres2 >= threshold)
    for pt in zip(*crossloc2[::-1]):
        bottom_right = (pt[0] + cross2.shape[1], pt[1] + cross2.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    crossloc3 = numpy.where(crossres3 >= threshold2)
    for pt in zip(*crossloc3[::-1]):
        bottom_right = (pt[0] + cross3.shape[1], pt[1] + cross3.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    leftcrossloc = numpy.where(leftcrossres >= threshold)
    for pt in zip(*leftcrossloc[::-1]):
        bottom_right = (pt[0] + leftcross.shape[1], pt[1] + leftcross.shape[0])
        cv2.rectangle(image, pt, bottom_right, (0, 255, 0), 2)

    # # Perform OCR on the screenshot
    pytesseract.pytesseract.tesseract_cmd = 'C:/Users/seeho/testadb/misc/Tesseract-OCR/tesseract.exe'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray, lang='eng', config='--psm 6 tessedit_char_unblacklist=0123456789')
    # cv2.imwrite('output.png', image)
    # Print the extracted text
    print(extracted_text)
    print(reset)
    # print(lap8loc[0].size)
    print(f"cloud3:{crossloc3[0].size}")
    print(f"cloud1:{crossloc[0].size}")
    print(f"cloud2:{crossloc2[0].size}")
    print(f"leftcross:{leftcrossloc[0].size}")

    # print("cloud:{}", crossres3)
    O_loc = numpy.where(numpy.array(extracted_text.split()) == "O")
    bracket_loc = numpy.where(numpy.array(extracted_text.split()) == "(_)")
    # print(state)
    # Clean up the screenshot file
    # os.remove('screen.png')

    if reset < 10 and ("PREMIUM CURRENCY" in extracted_text or "PREMIUMCURRENCY" in extracted_text):
        device.shell('input swipe 1990 385 2339 500')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1637 181')
        time.sleep(0.8)
        device.shell('input touchscreen tap 328 500')
        time.sleep(1)
        device.shell('input touchscreen tap 369 197')
        time.sleep(1)
        #reset
        device.shell('input touchscreen tap 1232 523')
        time.sleep(0.5)
        #confirmation
        device.shell('input touchscreen tap 1474 962')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1453 970')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1453 970')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1474 950')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1218 284')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1241 264')
        reset += 1
        #delete ADS
        # device.shell('input touchscreen tap 1182 535')
        # device.shell('input touchscreen tap 1214 704')
    
    elif reset >= 10 and "PREMIUM CURRENCY" in extracted_text:
        device.shell('input swipe 1990 385 2339 500')
        time.sleep(0.5)
        device.shell('input touchscreen tap 350 650')
        time.sleep(1)
        device.shell('input touchscreen tap 369 197')
        time.sleep(0.8)
        #delete ADS
        device.shell('input touchscreen tap 1182 735')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1214 904')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1232 577')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1474 928')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1218 282')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1241 264')
        time.sleep(0.5)
        device.shell('input touchscreen tap 1637 181')

        reset = 0

    elif "8 8 8 " in extracted_text or "=)" in extracted_text or "i)" in extracted_text:
        device.shell('input touchscreen tap 1637 181')


    elif "Reward granted" in extracted_text:
        device.shell('input touchscreen tap 2264 58')
    
    elif "O" in extracted_text and "Answer" in extracted_text and O_loc[0].size > 0:
        # Simulate a click using ADB at the center of the "Next" text
        center_x_next = int(image.shape[1] / 2)  # Center of the image
        center_y_next = int(image.shape[0] / 2)  # Center of the image
        device.shell(f"input touchscreen tap {center_x_next} {center_y_next}")
        time.sleep(0.5)
        device.shell('input touchscreen tap 2150 995')
    elif "(_)" in extracted_text and "Answer" in extracted_text and bracket_loc[0].size > 0:
        # Simulate a click using ADB at the center of the "Next" text
        center_x_next = int(image.shape[1] / 2)  # Center of the image
        center_y_next = int(image.shape[0] / 2)  # Center of the image
        device.shell(f"input touchscreen tap {center_x_next} {center_y_next}")
        time.sleep(0.5)
        device.shell('input touchscreen tap 2150 995')
        time.sleep(0.5)
        device.shell('input touchscreen tap 2150 995')

    elif (crossloc[0].size > 0 or crossloc2[0].size > 0 or leftcrossloc[0].size > 0):
        device.shell('input swipe 2339 385 1990 500')

        time.sleep(0.5)
        # device.shell(f"input touchscreen tap {center_x1} {center_y1}")
    # elif crossloc2[0].size > 0:
    #     time.sleep(0.5)
    #     device.shell(f"input touchscreen tap {center_x2} {center_y2}")   

    elif "Play" in extracted_text and ("new" in extracted_text or "Rate this app" in extracted_text or "Downloads" in extracted_text):
        device.shell('input swipe 2339 385 1990 500')
        time.sleep(0.2)
        device.shell('input touchscreen tap 1637 181') 

    elif crossloc3[0].size > 0 and crossloc3[0].size < 20:
        device.shell("input touchscreen tap 2280 62")

    # elif "Play" in extracted_text:
    #     device.shell('input swipe 2339 385 1990 500')
    #     time.sleep(0.5)

    



