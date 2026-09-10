import network
import time
from pico_secrets import WIFI_SSID, WIFI_PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

for attempt in range(15):
    if wlan.isconnected():
        break
    print("Connecting...")
    time.sleep(1)
else:
    print("Wi-Fi connection failed, status:", wlan.status())
    raise RuntimeError("Could not connect to Wi-Fi")

print(wlan.ifconfig())