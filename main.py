import pyautogui as pag
import cv2
import numpy as np

cordArray = []
screen = cv2.imread('Images\FullPizza1.png', cv2.IMREAD_UNCHANGED)
pizza = cv2.imread('Images\Pizza1.png', cv2.IMREAD_UNCHANGED)

def orders():
    return

"""
Returns the order of the penguins in the game in terms of coordinates.
@return: List of coordinates of the penguins in the game.
"""
def read():
    result = cv2.matchTemplate(screen, pizza, cv2.TM_CCOEFF_NORMED)
    cv2.imshow('Result', result)
    cv2.waitKey()
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    conf = 0.7
    yloc, xloc = np.where(result >= conf)
    len(yloc)
    print("Number of penguins:", len(yloc))
    w = pizza.shape[1]
    h = pizza.shape[0]
    cv2.rectangle( screen, max_loc, (max_loc[0] + w, max_loc[1]  + h), (0, 255, 255), 2)
    print("Location:", max_loc)
    print("Confidence:", max_val)
    cv2.imshow('Screen', screen)
    cv2.waitKey()
    return 

"""
Clicks on the penguins in the game in the order of the list of coordinates.
@param: List of the coordinates of the penguins in the game."""
def click(cordArray):
    return


"""
Runs the read function and then the click function when there are no more penguins present"""
def run():
    cordArray = read()
    click(cordArray)

read()