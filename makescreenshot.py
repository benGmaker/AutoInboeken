import pyautogui as gui  #needed for mouse and keyboard input
import time

if __name__ == '__main__':
    while True:
        print("Give Name for screenshot")
        screensavename = input()
        time.sleep(2)
        screenshot = gui.screenshot()
        screenshot.save(screensavename)
        print("screenshot made")
