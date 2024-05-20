import pyautogui as pag
import cv2
import numpy as np
import time
import keyboard

cordArray = []
screen = cv2.imread('Images/FullPizza1.png', cv2.IMREAD_UNCHANGED)
templates = [
    cv2.imread('Images/Pizza1.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('Images/Pizza2.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('Images/Pizza3.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('Images/Pizza4.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('Images/Pizza5.png', cv2.IMREAD_GRAYSCALE),
    cv2.imread('Images/Pizza6.png', cv2.IMREAD_GRAYSCALE)
]



def findOven():
    pizzaOven = cv2.imread('Images/PizzaOven.jpg', cv2.IMREAD_GRAYSCALE)
    screenshot = pag.screenshot()
    
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen, pizzaOven, cv2.TM_CCOEFF_NORMED)
    #cv2.imshow('Screen', screen)
    #cv2.waitKey()
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.5:
        print("Pizza Oven found at:", max_loc)
        return max_loc
    return None


"""
Returns the order of the penguins in the game in terms of coordinates.
@return: List of coordinates of the penguins in the game.
"""
def read():

    # Takes a screenshot of the screen
    # Take a screenshot of the screen
    screenshot = pag.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    
    #screen = cv2.imread('Images/FullPizza5.png', cv2.IMREAD_UNCHANGED)
    #screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
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
            #best_match = template
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
        #cv2.imshow('Screen', screen)
        #cv2.waitKey()  
        print("Coordinates:", coordinates)
        return coordinates
    else: # If no image passes the threshold
        return []


"""
Clicks on the penguins in the game in the order of the list of coordinates.
@param: List of the coordinates of the penguins in the game."""
def click(pizzaOven, cordArray):
    # 2880 x 1864
    print("Clicking")
    pag.click(pizzaOven[0], pizzaOven[1] - 200)
    print("Cord Array:" + str(cordArray))
    for cord in cordArray:
        print("Cord:" + str(cord))
        if not cord or len(cord[0]) != 4:
            continue
        x, y, w, h = cord[0]
        x += w // 2
        y += h // 2
        y += 100
        print("Clicking at:", x, y)
        pag.click(x, y)
        pag.click(1400, 930)
        time.sleep(0.2)


"""
Runs the read function, and appends the coordinates of the pizza to the list of coordinates, while making sure the same reading
isn't present twice in a row."""
def runRead():
    #global stop_program
    consecutive_failures = 0
    max_failed_attempts = 2
    while consecutive_failures < max_failed_attempts: #and not stop_program
        print("Attempt number:", consecutive_failures + 1)
        tempLocation = read()
        if tempLocation:
            consecutive_failures = 0
            if len(cordArray) == 0 or cordArray[-1] != tempLocation:
                cordArray.append(tempLocation)
                print(cordArray)
              # Reset the failure count
        else:  # If no coordinates are found
            consecutive_failures += 1
        
        #time.sleep(0.05)  # Wait for 0.1 seconds before the next read
def debug():
    screenshot = pag.screenshot()

    # Convert the screenshot to a format OpenCV can use
    screenshot_np = np.array(screenshot)
    screen = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # Print the size of the screenshot
    height, width, channels = screen.shape
    print(f"Screenshot size: {width} x {height}")

    # Display the screenshot using OpenCV
    cv2.imshow('Screenshot', screen)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()

def main():
    stop_key = 'q'
    pizzaOven = None
    while pizzaOven is None:
        print("Finding pizza oven")
        pizzaOven = findOven()
        time.sleep(0.1)
    while True:
        runRead()
        print(cordArray)
        if len(cordArray) > 0:
            click(pizzaOven, cordArray)
        #if keyboard.is_pressed(stop_key):  # Check if the stop key is pressed
         #   print(f"Stopped by user pressing '{stop_key}' key.")
          #  print(cordArray)
           # break



def main2():
    while True:
        read()
debug()
#main()
