from PIL import Image
import numpy as np
from art import *


import asciArtGenerator
import autoinboeken

Test_checkNoPop = False
Test_checkuserisknown = False

if __name__ == '__main__':

    if Test_checkNoPop: #Testing the checkNoPop function
        refPopImage = Image.open('TestData/snelstart.png') #load reference
        refPopBuf = np.asarray(refPopImage) #saving reference as array
        autoinboeken.checkNoPopUp(refPopBuf, "snelstart.png")
        autoinboeken.checkNoPopUp(refPopBuf, "boekhouden.png" )
        autoinboeken.checkNoPopUp(refPopBuf, "excelopsherm.png")
        autoinboeken.checkNoPopUp(refPopBuf, "klantingevuld.png")
        autoinboeken.checkNoPopUp(refPopBuf, "kleinepopup.png")
        autoinboeken.checkNoPopUp(refPopBuf, "metprompt.png")
        autoinboeken.checkNoPopUp(refPopBuf, "filled_in_article.png")

    if Test_checkuserisknown:
        autoinboeken.checkuserisnkown('klantingevuld.png') #screen with user found -> image sum = 91400
        autoinboeken.checkuserisnkown('snelstart.png') #screen without user found -> image sum = 122400

    asciArtGenerator.generateASCIart('ASCI-art/66logo.PNG')
    text = ' snelstart inboeken'
    font = 'tarty1'
    tprint('the 66th presents', 'smslant')
    tprint("versneldstart", font)
    tprint('inboeken', font)
