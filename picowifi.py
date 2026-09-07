import network
import time
from pico_secrets import WIFI_SSID, WIFI_PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

while not wlan.isconnected():
    print("Connecting...")
    time.sleep(1)

print(wlan.ifconfig())
wlan = network.WLAN(network.STA_IF)
print(wlan.isconnected())
print(wlan.ifconfig())