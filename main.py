import pyautogui as pag
import cv2
import numpy as np

cordArray = []
screen = cv2.imread('Images/FullPizza1.png', cv2.IMREAD_UNCHANGED)
templates = [
    cv2.imread('Images/Pizza1.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('Images/Pizza2.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('Images/Pizza3.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('Images/Pizza4.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('Images/Pizza5.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('Images/Pizza6.png', cv2.IMREAD_UNCHANGED)
]


def orders():
    return

"""
Returns the order of the penguins in the game in terms of coordinates.
@return: List of coordinates of the penguins in the game.
"""
def read():

    # Takes a screenshot of the screen
    # Take a screenshot of the screen
    screenshot = pag.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screen = cv2.imread('Images/FullPizza5.png', cv2.IMREAD_UNCHANGED)
    best_match = None
    best_confidence = 0
    best_location = None
    best_dimensions = None

    # Iterate through the templates
    for template in templates:
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > best_confidence:
            best_confidence = max_val
            best_match = template
            best_location = max_loc
            best_dimensions = (template.shape[1], template.shape[0])

    conf = 0.7

    if best_confidence >= conf: # If the confidence is greater than the threshold
        coordinates = []
        w, h = best_dimensions
        xloc, yloc = best_location
        coordinates.append((xloc, yloc, w, h))
        cv2.rectangle(screen, best_location, (xloc + w, yloc + h), (0, 255, 255), 2)
        print("Best match location:", best_location)
        print("Best confidence:", best_confidence)
        cv2.imshow('Screen', screen)
        cv2.waitKey()  
        return coordinates
    else: # If no image passes the threshold
        return []

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