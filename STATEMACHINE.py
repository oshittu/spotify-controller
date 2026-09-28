import SYMSCENE
import time
import HARDWARE

PAGE_HOME = 0
PAGE_SETTINGS = 1
PAGE_QUEUE = 2
PAGE_LIBRARY = 3

current_page = PAGE_HOME
page_just_changed = True


def run_home():
    global current_page, page_just_changed  # mandatory declaration

    if page_just_changed:
        SYMSCENE.drawHome()
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
    pass

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

def background_check():
    # check for wifi connectivity, update clock
    # will implement later
    pass


state_machine = {
    PAGE_HOME: run_home,
    PAGE_QUEUE: run_queue
}

while True:
    state_machine[current_page]()
    time.sleep(0.01)

        