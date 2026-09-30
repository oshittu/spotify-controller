import SYMSCENE
import time
import HARDWARE, urequests

PAGE_HOME = 0
PAGE_SETTINGS = 1
PAGE_QUEUE = 2
PAGE_LIBRARY = 3
PAGE_SCREENSAVER = 4
SERVER = "http://192.168.1.78:5000"

current_page = PAGE_SCREENSAVER
page_just_changed = True


def run_home():
    global current_page, page_just_changed  # mandatory declaration

    if page_just_changed:
        SYMSCENE.drawHome1()
        page_just_changed = False

    background_check()

    # button press handling
    if HARDWARE.b0.value():
        time.sleep(0.2)

    if HARDWARE.b1.value():
        time.sleep(0.2)

    if HARDWARE.b2.value():
        time.sleep(0.2)

    if HARDWARE.b3.value():
        SYMSCENE.homeNext()
        time.sleep(0.2)

    if HARDWARE.b4.value():
        time.sleep(0.2)

    if HARDWARE.b5.value():
        current_page = PAGE_QUEUE
        page_just_changed = True
        time.sleep(0.2)


def run_queue():
    if HARDWARE.b0.value():
        time.sleep(0.2)

    if HARDWARE.b1.value():
        time.sleep(0.2)

    if HARDWARE.b2.value():
        time.sleep(0.2)

    if HARDWARE.b3.value():
        time.sleep(0.2)

    if HARDWARE.b4.value():
        time.sleep(0.2)

    if HARDWARE.b5.value():
        time.sleep(0.2)

def run_screensaver():
    global current_page, page_just_changed  # mandatory declaration
    #background_check()
    #HARDWARE.testButtons()
    
    if page_just_changed:
        SYMSCENE.drawScreensaver()
        page_just_changed = False

    # button press handling
    if HARDWARE.b0.value():
        urequests.post(SERVER + "/previous")
        time.sleep(1)
        page_just_changed = True

    if HARDWARE.b1.value():
        urequests.post(SERVER + "/next")
        time.sleep(1)
        page_just_changed = True

    if HARDWARE.b2.value():
        urequests.post(SERVER + "/play/Alexa")
        time.sleep(0.2)

    if HARDWARE.b3.value():
        urequests.post(SERVER + "/play/Google")
        time.sleep(0.2)

    if HARDWARE.b4.value():
        time.sleep(0.2)

    if HARDWARE.b5.value():
        pass
        # current_page = PAGE_QUEUE
        # page_just_changed = True
        # time.sleep(0.2)
    
    
def background_check():
    global current_page, page_just_changed  # mandatory declaration

    # checkSpotifyConnectivity()
    # checkWifiConnectivity()
    checkSongChange() # to trigger cover change
    

def checkSpotifyConnectivity():
    # run a simple spotify api call over and over til its connected
    pass

def checkSongChange():
    currentSong = apicall()

    while(True):
        songPlaying = apicall()
        if currentSong is not songPlaying:
            return True
        time.sleep(5)

state_machine = {
    PAGE_HOME: run_home,
    PAGE_QUEUE: run_queue,
    PAGE_SCREENSAVER: run_screensaver
}

while True:
    state_machine[current_page]()
    time.sleep(0.01)