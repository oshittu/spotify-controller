import picowifi
import butMonkey
import HARDWARE, STATEMACHINE

picowifi.connect()
STATEMACHINE.run_home()