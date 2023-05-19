import pyautogui as gui  #needed for mouse and keyboard input
import pandas as pd #needed for reading data
import time
from PIL import Image
import numpy as np

def readdata(file):
    df = pd.read_excel(file)
    #print(df) #we need column 4 and 5
    #from column 4 we need everything between ( and )
    personen = df.iloc[:,3]
    PLU = df.iloc[:,4]

    dates = df.iloc[:,0]

    #if dates[0] <= dates[len(dates)-1]:
        #raise Exception('Wrong data selected')

    #controleren of de data goed geselecteerd is.
    if personen.name != "Persoon":
        raise Exception('Wrong data selected')

    if PLU.name != "PLU":
        raise Exception('Wrong data selected')

    if len(PLU) != len(personen):
        raise Exception('Wrong data selected')


    ID = personen.apply(lambda st: st[st.find("(")+1:st.find(")")]) #extracting user unique ID's
    return ID, PLU, personen

#locaties op het scherm
klantX = 280
klantY = 280
artikelX = 90
artikelY = 720
omschrijvingX = 666
omschrijvingY = 495
def insertData(userID,plu):
    #inputdata writes down the userID and plu into the correct boxes
    gui.click(klantX,klantY)
    gui.typewrite(userID)
    time.sleep(0.1) #sleep to slow down program
    gui.click(artikelX,artikelY)
    gui.typewrite(str(plu))
    time.sleep(0.1)

#ranges that user name should appear in if the user is known to snelstart
correctuserY = 285
correctuserX1 = 350
correctuserX2 = 470
colorsumZonderKlant = 91800
margin = 2000
def checkuserisnkown(TestReference = "noref"):
    debug = False
    if TestReference != "noref": #checking if we are in debug mode
        debug = True

    if debug: #loading debug image or taking screenshot
        image = Image.open(TestReference)
    else:
        screenshot = gui.screenshot()
        screenshot.save("klantCheck.png")
        time.sleep(0.1)  # sleep to slow down program
        #Vo
        image = Image.open('TestData/klantCheck.png');  # loading in the screenshot

    colorsum = 0
    for i in range(correctuserX1,correctuserX2):
        colorsum = colorsum + sum(image.getpixel((i,correctuserY)) )

    if debug:
        print(colorsum)

    if colorsum < colorsumZonderKlant - margin:
        return True
    else:
        return False

def insertUnkownUser(userID):
    #removes user from box and insert unkown user, adds user id to description
    #removing data in klant
    gui.click(klantX, klantY)
    gui.hotkey("ctrl","a")
    gui.press("backspace")
    gui.typewrite("2") #insert unkown user

    gui.click(omschrijvingX,omschrijvingY)
    gui.typewrite(userID)

def confirmInboeken():
    gui.press("F5")
    gui.hotkey("ALT","N")
    time.sleep(8) #wait 8 second to print contantbon

Threshold = 14345678
def checkNoPopUp(refPopBuf, TestReference = "noref"):
    debug = False
    if TestReference != "noref": #checking if we are in debug mode
        debug = True
    time.sleep(0.5)
    while True:
        if debug:#loading debug image or taking screenshot
            print(TestReference)
            image = Image.open(TestReference)
        else:
            screenshot = gui.screenshot()  # making screenshot
            screenshot.save("popupCheck.png")
            time.sleep(0.1)
            image = Image.open("TestData/popupCheck.png")

        time.sleep(0.1)  # sleep to slow down program
        BufferCheck = np.asarray(image)# loading screenshot in as array
        Difference = BufferCheck[300:1080, 1:1900] - refPopBuf[300:1080, 1:1900] #getting the differnce between image and refrence
        greyscale = np.sum(Difference, 2)
        result = np.sum(greyscale) #resulting collor difference value
        if result <= Threshold:
            if debug:
                #im = Image.fromarray(greyscale)
                #im.show()
                print('NO POPUP DETECTED')
                print(result)
            return
        else:
            print("pop up detected")

        #Exiting for loop if in debug mode
        if debug:
            #im = Image.fromarray(greyscale)
            #im.show()
            print(result)
            return

        time.sleep(1) # wait before checking again if popup has cleared

if __name__ == '__main__':
    print('Insert Name Excel Sheet')
    filename = input()
    if filename.endswith('.xlsx') != True:
        filename = filename + ".xlsx"
    refPopImage = Image.open('TestData/snelstart.png') #load reference
    refPopBuf = np.asarray(refPopImage)

    ID, PLU, personen = readdata(filename)
    time.sleep(5) #delay such that you can change screen
    for i in range(len(ID)):
        insertData(ID[i],PLU[i]) #Fill in username and product
        gui.click(omschrijvingX, omschrijvingY) #click away such that the omschrijving is not blue
        checkNoPopUp(refPopBuf)  # Check if there is no popup
        if checkuserisnkown() != True:
            insertUnkownUser(personen[i])
        confirmInboeken() #print contantbon
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