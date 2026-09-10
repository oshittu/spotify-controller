awesome vibe coded project #2
if done well this can be MODERN DAY IPOD!!! 
currently this awesome project displays a cute monkey while controlling spotify playback (CURRENT VERSION: V2)

Quick Start (only start Lol)
1. assemble hardware
2. start fast api server copy paste this into powershell
    uvicorn fartify:app --host 0.0.0.0 --port 5000
3. connect pico to wifi if you havent already by running picowifi.py
4. run picoPart.py on the pico
5. eureka 

TOMI TODO
> Up and down control volume
> left and right skip song

Later
> Digital interface

V1
    1. Physical assembly                    - DONE
        > Previous and next buttons
        > Screen integration (for fun)
    2. Spotify, Wireless Integration        - DONE
    3. (optional) Graphic interface         - Monkey Done, real work TBD

V2
    1. Pico can connect to spotify independently without my http host
    2. MAKE A PROGRAM TO DEAL WITH WIFI CUTOUTS AND RECONNECTION
    3. make an actually good graphic interface
        > how do i deal with scene switching etc? looking for a good library...
        > A: smtg like a state machine? 
