import pyautogui
import pydirectinput
import random
import time
import datetime

def click(imgfile, max_tries=30):
    attempts = 0
    while attempts < max_tries:
        time.sleep(1.6)
        res = pyautogui.locateCenterOnScreen(imgfile, confidence=0.7)
        if res is None:
            print(f"\rButton {imgfile} not found on attempt {attempts}/{max_tries}", end="")
            attempts += 1
        else:
            break
        if attempts % 10 == 0:
            # if opponent disconnected, catch it here and re-enter lobby
            exiter = pyautogui.locateCenterOnScreen('assets/exit.png', confidence=0.7)
            if exiter is not None:
                print(f'\rExiting {imgfile} due to opponent disconnect')
                pyautogui.click(exiter.x, exiter.y)
                return 'restart'
            # if we disconnected, catch it here and re-enter lobby
            exiter = pyautogui.locateCenterOnScreen('assets/disconnect.png', confidence=0.7)
            if exiter is not None:
                print(f'\rExiting {imgfile} due to network disconnect')
                pyautogui.click(exiter.x, exiter.y)
                return 'restart'  # resturn restart if we disconnected
    if res is not None:
        print(f'\rFound {imgfile} on attempt {attempts}/{max_tries}' + ' ' * 12)
        for i in range(3):
            pyautogui.click(res.x, res.y)
            time.sleep(1)
        return (res.x, res.y)  # return the xy coordinates of the button if we click
    print(f'\rUnable to find button {imgfile} after {max_tries} attempts, proceeding to next step')
    return None  # return None if we didn't click anything

def place_tower(key, player, attempts=20, emote=()):
    win_corner = pyautogui.locateCenterOnScreen("assets/window_title.png", confidence=0.8)
    if player == 0:
        xmin, ymin = win_corner.x + 150, win_corner.y + 100
        xmax, ymax = win_corner.x + 800, win_corner.y + 940
    else:
        xmin, ymin = win_corner.x + 1000, win_corner.y + 100
        xmax, ymax = win_corner.x + 1450, win_corner.y + 940
    for i in range(attempts):
        res = pyautogui.locateCenterOnScreen("assets/ok.png", confidence=0.7)
        if res is not None:
            return False
        pydirectinput.press('r') # cycle to offhand tower (dart) to change position of desired tower
        pydirectinput.press(key)
        x, y = random.randrange(xmin, xmax), random.randrange(ymin, ymax)
        pyautogui.click(x, y)
        
        if len(emote) > 0:
            pydirectinput.keyDown('ctrl')
            pydirectinput.press(str(emote[i % (len(emote) - 1)]))  # bloon boost
            pydirectinput.keyUp('ctrl')
    return True

loop = 0
while True:
    print(f"{datetime.datetime.now()} Successful Games: {loop}")
    # queue into battle
    if click("assets/battle.png") == 'restart':
        continue
    if click("assets/ready.png") == 'restart':
        continue
    if click("assets/battle2.png") == 'restart':
        continue

    time.sleep(6)  # wait for battle to start
    # once in battle, send bloons and place towers
    coords = click("assets/redbloon.png")  # wait for round to start
    if coords is not None and len(coords) == 2:
        x, y = coords
        player = 0 if x < 500 else 1
        pydirectinput.press('a', presses=5, interval=0.125)  # send red bloon rush

        for i in range(5):
            pydirectinput.press('s')  # layer blue bloons
            shouldcontinue = place_tower("q", player, attempts=2)  # randomly place hero
            pydirectinput.keyDown('ctrl')
            pydirectinput.press('space')  # bloon boost
            pydirectinput.keyUp('ctrl')
            pydirectinput.press('space')  # tower boost
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('3')  # bm
        pydirectinput.keyUp('ctrl')
        if shouldcontinue is not None:  # if the game ended already, stop placing towers
            shouldcontinue = place_tower("w", player, attempts=10)  # randomly place 3rd tower
        if shouldcontinue is not None:  # if the game ended already, stop placing towers
            shouldcontinue = place_tower("e", player, attempts=80, emote=[9, 4])  # randomly place 1st tower
        # if shouldcontinue:
        #     click("assets/surrender.png", max_tries=3)
        #     time.sleep(2)
        #     click("assets/confirm.png", max_tries=3)
    if click("assets/ok.png", max_tries=128) == 'restart':  # wait until you leak to death and the win screen pops up. this may take a while
        continue
    loop += 1
    click("assets/discard.png", max_tries=3)  # in case we recieve a chest, discard it
    click("assets/back.png", max_tries=3)  # back to main menu
