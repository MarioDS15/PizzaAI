import pyautogui as pag
import cv2
import numpy as np
import time
from tkinter import Tk, Label
from PIL import ImageTk, Image
import threading
from arrays import *

# Constants
ORDER_COOLDOWN = 0.1
last_seen_times = {}
cordArray = []
verifiedArray = []

screen = cv2.imread('Images/FullPizza1.png', cv2.IMREAD_UNCHANGED)
templates = [
    cv2.imread('Images/Pizza1.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('Images/Pizza2.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('Images/Pizza3.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('Images/Pizza4.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('Images/Pizza5.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('Images/Pizza6.png', cv2.IMREAD_GRAYSCALE)
]



def click(pizzaOven, cordArray):
    current_time = time.time()

    pag.click(pizzaOven[0], pizzaOven[1])
    print("Index of penguins:" + str(cordArray))

    for cord in cordArray:
        time.sleep(0.1)
        if not cord or len(cord[0]) != 4:
            continue
        if cord == []:
            continue
        #print("Looking to click:" + str(cord))
        x, y, w, h = cord[0]
        x += w // 2
        y += h // 2
        y += 100

        coord_key = (x, y)

        #print("Clicking at:", x, y)
        pag.click(x, y)

def findRetry():
    retry = cv2.imread('Images/Replay.png', cv2.IMREAD_GRAYSCALE)
    screenshot = pag.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen, retry, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.6:
        print("Retry button found at:", max_loc)
        return max_loc
    return None


def checkFailed():
    return

def findOven():
    pizzaOven = cv2.imread('Images/PizzaOvenWin.png', cv2.IMREAD_GRAYSCALE)
    screenshot = pag.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen, pizzaOven, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.5:
        print("Pizza Oven found at:", max_loc)
        return max_loc
    return None


def read(start_time):
    global cordArray
    screenshot = pag.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

    best_match = None
    best_confidence = 0
    best_location = None
    best_dimensions = None

    for template in templates:
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > best_confidence:
            best_confidence = max_val
            best_location = max_loc
            best_dimensions = (template.shape[1], template.shape[0])

    conf = 0.8
    if best_confidence >= conf:
        coordinates = []
        w, h = best_dimensions
        xloc, yloc = best_location
        coordinates.append((xloc, yloc, w, h))
        cv2.rectangle(screen, best_location, (xloc + w, yloc + h), (0, 255, 255), 2)
        current_time = time.time()
        elapsed_time = current_time - start_time
        #print(f"Coordinates at {elapsed_time:.2f} seconds: {coordinates}")
        cordArray.append(coordinates)
    else:
        cordArray.append([])


def call_read_every_n_seconds(n, x, stop_event, start_time):
    def run():
        consecutive_empty_returns = 0
        global cordArray  # Use global cordArray
        
        while consecutive_empty_returns < x and not stop_event.is_set():
            start_time_loop = time.time()
            read(start_time)  # Pass the program start time to read
            
            if cordArray and not cordArray[-1]:  # Check the last appended result in cordArray if not empty
                consecutive_empty_returns += 1
                #print(f"No match found. Consecutive empty returns: {consecutive_empty_returns}")
            else:
                consecutive_empty_returns = 0  # Reset counter if a match is found
            
            elapsed_time = time.time() - start_time_loop
            sleep_time = max(0, n - elapsed_time)
            time.sleep(sleep_time)
        
        #print("Stopping the thread after reaching the maximum consecutive empty returns.")
        stop_event.set()  # Signal that the thread has finished

    thread = threading.Thread(target=run)
    thread.daemon = True  # Daemonize thread to allow program to exit even if thread is running
    thread.start()
    return thread


def main():
    global cordArray, verifiedArray  # Declare cordArray as global to modify it inside main
    cordArray = []  # Initialize cordArray
    
    program_start_time = time.time()  # Capture the program's start time
    
    # Placeholder for finding the pizza oven
    pizzaOven = None

    while pizzaOven is None:
        pizzaOven = findOven()
        time.sleep(0.1)

    retryLoc = None

        
    while True:
        cordArray = []  # Reset cordArray for each run
        stop_event = threading.Event()
        call_read_every_n_seconds(0.1, 4, stop_event, program_start_time)
        while retryLoc is None:
            retryLoc = findRetry()
        stop_event.wait()  # Wait for the reading thread to finish
        cordArray = organize(cordArray)
        #print("Verified Array:", verifiedArray)
        #print("Cord Array:", cordArray)
        if verifiedArray == []:
            verifiedArray = cordArray
        else:
            if len(verifiedArray) == len(cordArray):
                time.sleep(0.2)
                pag.click(retryLoc[0] + 30, retryLoc[1] + 30)
                continue
            else:
                verifiedArray.append(cordArray[-1])

        print("Clicking")
        click(pizzaOven, verifiedArray)
        print("Thread has stopped. Proceeding with the next iteration.")
        time.sleep(0.1)  


main()