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

if __name__ == '__main__':
    test_checkuseriskown()
    test_checknopopup()

    asciArtGenerator.generateASCIart('ASCI-art/66logo.PNG')
    text = ' snelstart inboeken'
    font = 'tarty1'
    tprint('the 66th presents', 'smslant')
    tprint("versneldstart", font)
    tprint('inboeken', font)
