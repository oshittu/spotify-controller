import SYMSCENE

PAGE_HOME = 0
PAGE_SETTINGS = 1
PAGE_QUEUE = 2
PAGE_LIBRARY = 3

current_page = PAGE_HOME
page_just_changed = True

def drawL_homescreen():
    SYMSCENE.drawHome()

def drawL_settings():
    print

def drawL_queue():
    print

def drawL_library():
    print

while True:
    if current_page == PAGE_HOME:
        if page_just_changed:
            drawL_homescreen()
            page_just_changed = False

        update_clock()

        if settings_button_pressed():
            current_page = PAGE_SETTINGS
            page_just_changed = True

    elif current_page == PAGE_SETTINGS:
        if page_just_changed:
            drawL_settings()
            page_just_changed = False

        