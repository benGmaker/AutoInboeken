import pandas as pd
from PIL import Image
import numpy as np
from art import *

import asciArtGenerator
import autoinboeken

def test_checkuseriskown():
    print("--------------------------------")
    print("Testing checkuseriskown")
    print(autoinboeken.checkuserisnkown('TestData/klantingevuld.png'))  # screen with user found -> image sum = 91400
    print(autoinboeken.checkuserisnkown('TestData/snelstart.png'))  # screen without user found -> image sum = 122400

def test_checknopopup():
    print("--------------------------------")
    print("Testing checknopopup")
    #testing the checkNoPopUp function to calibrate thee Threshold value for having a popup
    refPopImage = Image.open('TestData/snelstart.png')  # load reference
    refPopBuf = np.asarray(refPopImage)  # saving reference as array

    #Checking what kind of values we get
    autoinboeken.checknopopup(refPopBuf, "TestData/snelstart.png") #no popup
    autoinboeken.checknopopup(refPopBuf, "TestData/filled_in_article.png")  # no popup
    autoinboeken.checknopopup(refPopBuf, "TestData/klantingevuld.png") #no popup
    autoinboeken.checknopopup(refPopBuf, "TestData/boekhouden.png")
    autoinboeken.checknopopup(refPopBuf, "TestData/excelopsherm.png")
    autoinboeken.checknopopup(refPopBuf, "TestData/kleinepopup.png")
    autoinboeken.checknopopup(refPopBuf, "TestData/metprompt.png")

path_log = lambda plu, artikelnaam : "log/" + str(plu) + " " + artikelnaam + ".xlsx"
TEST_PLU = 66
TEST_ARTIKEL = "HULDE&VO"
TEST_MOLLIE_ID = 'mollie_ABC123'
def test_checklog():
    print("--------------------------------")
    print("Testing checklog")
    df = pd.DataFrame() #emptying any existing data
    df.to_excel(path_log(TEST_PLU,TEST_ARTIKEL))
    # writing 1 entry in the logbook
    autoinboeken.log_inboeken(TEST_PLU,TEST_ARTIKEL,TEST_MOLLIE_ID, 1445758, "Ben Gortemaker", 1)
    #performing tests
    print(autoinboeken.checklog(TEST_PLU, TEST_ARTIKEL, TEST_MOLLIE_ID,1)) #True
    print(autoinboeken.checklog(TEST_PLU, TEST_ARTIKEL, TEST_MOLLIE_ID, -1)) #False
    print(autoinboeken.checklog(TEST_PLU, TEST_ARTIKEL, TEST_MOLLIE_ID, 66))  #False
    print(autoinboeken.checklog(TEST_PLU, TEST_ARTIKEL, "ander_mollie_id",1)) #False

def test_log_inboeken():
    print("--------------------------------")
    print("Testing log_inboeken")
    autoinboeken.log_inboeken(661, "mooie voorzitters", "mollie_ABC123", 1445758, "Ben Gortemaker", 1)

def asciart():
    asciArtGenerator.generateASCIart('ASCI-art/66logo.PNG')


def test_GUI():
    gui = autoinboeken.CLI_GUI();
    gui.startupscreen(1)
    gui.printlogo()

if __name__ == '__main__':
    #test_GUI()
    #test_checkuseriskown()
    #test_checknopopup()
    #test_log_inboeken()
    #test_checklog()



