import pyautogui as gui  #needed for mouse and keyboard input
import pandas as pd #needed for reading data
import time
import csv
from PIL import Image
import numpy as np

def readdata(file):
    if file.endswith('.xlsx') != True: #adding extension if needed
        file = file + ".xlsx"
    df = pd.read_excel(file) #reading in the data
    plu = df.iloc[:, 4]
    personen = df.iloc[:, 3]
    id = personen.apply(lambda st: st[st.find("(") + 1:st.find(")")])  # extracting user unique ID's
    mollie_ID = df.iloc[:,1]
    aantal = df.iloc[:,5]
    artikelnaam = df.iloc[:,2]

    # Checking if data has correctly been selected
    if personen.name != "Persoon":
        raise Exception('Persoon header row not in the data')
    if plu.name != "PLU":
        raise Exception('PLU header row not in the data')
    if len(plu) != len(personen):
        raise Exception('PLU en personen data unequal length')

    return id, plu, personen, aantal, mollie_ID, artikelnaam  #returning selected data

#locaties op het scherm
KLANT_X = 280
KLANT_Y = 280
ARTIKEL_X = 90
ARTIKEL_Y = 720
OMSCHRIJVING_X = 666
OMSCHRIJVING_Y = 495
def insert_data(user_id, plu):
    #inputdata writes down the userID and plu into the correct boxes
    gui.click(KLANT_X, KLANT_Y)
    gui.typewrite(user_id)
    gui.click(ARTIKEL_X, ARTIKEL_Y)
    gui.typewrite(str(plu))

#ranges that user name should appear in if the user is known to snelstart

def insert_unkown_user(userID):
    #removes user from box and insert unkown user, adds user id to description
    #removing data in klant
    gui.click(KLANT_X, KLANT_Y)
    gui.hotkey("ctrl","a")
    gui.press("backspace")
    gui.typewrite("2") #insert unkown user

    gui.click(OMSCHRIJVING_X, OMSCHRIJVING_Y)
    gui.typewrite(userID)

CORRECTUSER_Y = 285
CORRECTUSER_X1 = 350
CORRECTUSER_X2 = 470
UNKOWNUSER_COLORSUM = 91800
UNKOWNUSER_MARGIN = 2000
def checkuserisnkown(test="notest"):
    debug = False
    if test != "notest":  # checking if we are in debug mode
        print(test)
        debug = True

    if debug:  # loading debug image or taking screenshot
        image = Image.open(test)
    else:
        screenshot = gui.screenshot()
        screenshot.save("klantCheck.png")
        image = Image.open('TestData/klantCheck.png');  # loading in the screenshot

    colorsum = 0
    for i in range(CORRECTUSER_X1, CORRECTUSER_X2):
        colorsum = colorsum + sum(image.getpixel((i, CORRECTUSER_Y)))

    if debug:
        print(colorsum)

    if colorsum < UNKOWNUSER_COLORSUM - UNKOWNUSER_MARGIN:
        return True
    else:
        return False

NOPOPUP_THRESSHOLD = 14345678
def checknopopup(refpop_buf, test="notest"):
    debug = False
    if test != "notest":  # checking if we are in debug mode
        debug = True
    time.sleep(0.5)
    while True:
        if debug:  # loading debug image or taking screenshot
            print(test)
            image = Image.open(test)
        else:
            screenshot = gui.screenshot()  # making screenshot
            screenshot.save("popupCheck.png")
            image = Image.open("TestData/popupCheck.png")

        check_buff = np.asarray(image)  # loading screenshot in as array
        difference = check_buff[300:1080, 1:1900] - refpop_buf[300:1080,
                                                    1:1900]  # getting the differnce between image and refrence
        greyscale_diff = np.sum(difference, 2)
        result = np.sum(greyscale_diff)  # resulting collor difference value
        if result <= NOPOPUP_THRESSHOLD:
            if debug:
                # im = Image.fromarray(greyscale) #showing image takes long
                # im.show()
                print('NO POPUP DETECTED')
                print(result)
            return
        else:
            print("POPUP DETECTED")

        if debug:  # Exiting for loop if in debug mode
            # im = Image.fromarray(greyscale)
            # im.show()
            print(result)
            return

        time.sleep(1)  # wait before checking again if popup has cleared
        print("Checking again")

def checklog(plu,artikelnaam,mollie_ID):
    file = "log/" + plu + " " + artikelnaam + ".txt"
    try
    open()

def confirm_inboeken():
    gui.press("F5")
    gui.hotkey("ALT","N")
    time.sleep(8) #wait 8 second to print contantbon

if __name__ == '__main__':
    print('Insert Name Excel Sheet')
    filename = input()
    refpop_im = Image.open('TestData/snelstart.png') #loading reference
    refpop_buf = np.asarray(refpop_im) #creating refrence buffer

    id, plu, personen, aantal, mollie_ID, artikelnaam= readdata(filename)
    time.sleep(2) #delay such that you can change screen
    for i in range(len(id)):
        #check if data is in logbook
        insert_data(id[i], plu[i]) #Fill in username and product
        gui.click(OMSCHRIJVING_X, OMSCHRIJVING_Y) #click away such that the omschrijving is not blue
        checknopopup(refpop_buf)  # Check if there is no popup
        if checkuserisnkown() != True:
            #insert in unkownuserlogbook
            insert_unkown_user(personen[i])
        #insert data in logbook
        confirm_inboeken() #print contantbon
        #locaties

    print("Inboeken Completed")


#TODO
# * GUI maken    fff
#   - Startupscreen met allemaal 66 vo dingen
#   - Countdown timer voor het beginnen
#   - Ergens popup laten zien waar hij mee bezig is
#   - Contact info van mij laten zien
# * Het aantal column laten invullen (mensen uitboeken/meerdere dingen kopen) (if not equal 1)
# * Exporteren onbekende klanten
# * Inboeken op autoinboek medewerker
# * Implementeren dat hij makkelijk geen bonnetjes laat printen #gogreen
# * FINAL Compilen van code naar een EXE
# * Website direct de excel laten downloaden