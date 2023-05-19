import pyautogui as gui  #needed for mouse and keyboard input
import pandas as pd #needed for reading data
import time
from PIL import Image
import numpy as np
import os
import sys
import art
from colorama import Fore, Back, Style

FONT1 = 'tarty1'
FPS = 10
class CLI_GUI:
    def __init__(self):
        self.text1 = art.text2art(text = 'the 66th presents',font = 'smslant')
        self.text2 = art.text2art(text = "versneldstart", font = FONT1)
        self.text3 = art.text2art(text = "inboeken", font = FONT1)
        self.text4 = art.text2art(text = '     Accelerated!',font = 'smslant')
    def startupscreen(self, duration = 1    ):
        print(Style.BRIGHT + " ")
        d = 12
        for i in range(FPS*duration):
            ofset = i*3
            os.system('cls')
            self.printcolorcycle(self.text1, 10, ofset)
            self.printcolorcycle(self.text2, 12, ofset)
            self.printcolorcycle(self.text3, 10, ofset)
            time.sleep(1 / FPS)

    def printcolorcycle(self,text, basediv = 3, offset = 0):
        count = offset
        for i in text:

            remainder = np.floor(count/basediv%3) #devide by three and round down
            if remainder == 0:
                sys.stdout.write(Fore.BLUE + i)
            if remainder == 1:
                sys.stdout.write(Fore.YELLOW + i)
            if remainder == 2:
                sys.stdout.write(Fore.BLUE   + i)
            count += 1

    STEPS = 1003
    DURATION = 0.01
    def printlogo(self):
        with open("readme.txt", "r") as f:
            logo = f.read()
        print(" ")
        step = len(logo) // self.STEPS
        for i in range(self.STEPS):
            sys.stdout.write(Fore.BLUE + logo[i*step+1:(i+1)*step])
            time.sleep(self.DURATION/self.STEPS)
        print(("made by Ben Gortemaker, Chairman & Editor-in-Chief of the 66th Board"))
        print(Fore.YELLOW + self.text4)

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
    #vo
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

AANTAL_X = 760
AANTAL_Y = 720
def insert_aantal(aantal):
    gui.click(AANTAL_X,AANTAL_Y)
    gui.typewrite(aantal)

VERKOPER_DROPDOWN_X = 808
VERKOPER_DROPDOWN_Y = 600
AUTO_INBOEKER_X = 0
AUTO_INBOEKER_Y = 0
def select_verkoper():
    gui.click(VERKOPER_DROPDOWN_X,VERKOPER_DROPDOWN_Y)
    gui.CLICK(AUTO_INBOEKER_X, AUTO_INBOEKER_Y)

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

path_log = lambda plu, artikelnaam : "log/" + str(plu) + " " + artikelnaam + ".xlsx"

def checklog(plu,artikelnaam,mollie_ID, aantal):
    #Returns false if inboek operation has not been found in the logbook
    path = path_log(plu, artikelnaam)
    try: #try to find the logbook
        df = pd.read_excel(path)
    except:
        print("no log found")
        return False #there is no log, thus the inboek operation is not found

    if mollie_ID in df["Mollie-ID"].unique(): #checking if the mollie ID is in the logbook
        df = df.set_index("Mollie-ID")#set the mollie ID as index
        if df.loc[mollie_ID]['Aantal']== aantal: #checking if the aantal matches
            #this only works if any given operation is only once in the log book, if it is in there twice it will throw an exception
            return True #same operation has been found in the log
    return False #the inboek operation has not been found in the log

LOG_CSV_COLUMNS = ["Mollie-ID", "ID-nummer", "Naam", "Aantal"]
def log_inboeken(plu,artikelnaam,mollie_ID,id,persoon,aantal):
    path = path_log(plu, artikelnaam)

    try: df = pd.read_excel(path)
    except:
        df = pd.DataFrame(columns=LOG_CSV_COLUMNS)
        print('new log file created')
    new_row = {"Mollie-ID": mollie_ID, "ID-nummer": id, "Naam": persoon, "Aantal": aantal}
    df = df.append(new_row, ignore_index=True)
    df.to_excel(path, index=False)

def confirm_inboeken():
    gui.press("F5")
    gui.hotkey("ALT","N")
    time.sleep(8) #wait 8 second to print contantbon

if __name__ == '__main__':
    cli_gui = CLI_GUI()
    cli_gui.startupscreen(1)
    print('\n Insert Name Excel Sheet')
    filename = input()
    refpop_im = Image.open('TestData/snelstart.png') #loading reference
    refpop_buf = np.asarray(refpop_im) #creating refrence buffer
    id, plu, personen, aantal, mollie_ID, artikelnaam= readdata(filename)
    cli_gui.printlogo()

    for i in range(len(id)):
        if checklog(plu[i],artikelnaam[i],mollie_ID[i], aantal[i]):#checking if inboek operation already has been done
            message = str(aantal[i]) + " x " + str(plu[i]) + personen[i] + "is already booked in"
            raise(message) #raising exception
        insert_data(id[i], plu[i]) #Fill in username and product
        gui.click(OMSCHRIJVING_X, OMSCHRIJVING_Y) #click away such that the omschrijving is not blue
        checknopopup(refpop_buf)  #Check if there is no popup
        if checkuserisnkown() != True:
            log_inboeken(plu[i],"onbekend" + artikelnaam[i],mollie_ID[i],id[i],personen[i],aantal[i])#insert in unkownuserlogbook
            insert_unkown_user(personen[i]) #inserting unkown user
        if aantal[i] != 1:insert_aantal(aantal[i]) #if aantall is other than 1 insert in aantal field
        select_verkoper()
        log_inboeken(plu[i],artikelnaam[i],mollie_ID[i],id[i],personen[i],aantal[i])#insert data in logbook

        confirm_inboeken() #print contantbon
        print("booked in {}x {}, {}, ({}) {}".format(aantal[i], plu[i],artikelnaam[i],id[i],personen[i],))
    cli_gui.printlogo()
    print("Inboeken has succesfully been Accererated!")