import network
import time
from pico_secrets import WIFI_SSID, WIFI_PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

def connect():
    for attempt in range(15):
        if wlan.isconnected():
            ip = wlan.ifconfig()[0] # the pico w's ip is the first returned address
            print(f"Connected @ {ip}")
            break
        print("Connecting...")
        time.sleep(1)
    else:
        print("Wi-Fi connection failed, status:", wlan.status())
        raise RuntimeError("Could not connect to Wi-Fi")
    print(wlan.ifconfig())
    return True

def isConnected():
    if wlan.isconnected():
        return True
    return False