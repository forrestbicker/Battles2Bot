import pyautogui
import pydirectinput
import random
import time


def click(imgfile, max_tries=30):
    attempts = 0
    while attempts < max_tries:
        time.sleep(1.6)
        res = pyautogui.locateCenterOnScreen(imgfile, confidence=0.7)
        if res is None:
            print(f"Button {imgfile} not found on attempt {attempts}/{max_tries}")
            attempts += 1
            continue
        break
    if res is not None:
        for i in range(3):
            pyautogui.click(res.x, res.y)
            time.sleep(1)
        return True
    return False

def place_tower(key):
    win_corner = pyautogui.locateCenterOnScreen("BTDB2Bot/window_title.png", confidence=0.8)
    xmin, ymin = win_corner.x + 100, win_corner.y + 100
    xmax, ymax = win_corner.x + 1450, win_corner.y + 940
    for i in range(20):
        res = pyautogui.locateCenterOnScreen("BTDB2Bot/round.png", confidence=0.7)
        if res is None:
            return False
        pydirectinput.press(key)
        x, y = random.randrange(xmin, xmax), random.randrange(ymin, ymax)
        pyautogui.click(x, y)
    return True



while True:
    # queue into battle
    click("BTDB2Bot/battle.png")
    click("BTDB2Bot/ready.png")
    click("BTDB2Bot/battle2.png")
    if click("BTDB2Bot/disconnect.png", max_tries=3):  # if opponent disconnected, catch it here and re-enter lobby
        continue

    time.sleep(6) # wait for battle to start
    # once in battle, send bloons and place towers
    click("BTDB2Bot/redbloon.png")  # wait for round to start
    [pydirectinput.press('a') for i in range(5)]  # send red bloon rush
    [pydirectinput.press('s') for i in range(2)]  # layer blue bloons

    shouldcontinue = place_tower("q")  # randomly place hero
    if shouldcontinue:  # if the game ended already, stop placing towers
        place_tower("w")  # randomly place 1st tower
    # if shouldcontinue:
    #     time.sleep(28)
    #     click("BTDB2Bot/surrender.png", max_tries=4)
    #     time.sleep(2)
    #     click("BTDB2Bot/confirm.png", max_tries=4)
    click("BTDB2Bot/ok.png", max_tries=64)  # wait until you leak to death and the win screen pops up. this may take a while
    click("BTDB2Bot/discard.png", max_tries=3)  # in case we recieve a chest, discard it
    click("BTDB2Bot/back.png", max_tries=3)  # back to main menu
