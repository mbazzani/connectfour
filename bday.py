import pyjokes
import time
import os
import connectfour
from PIL import Image

while True:
    os.system("clear")
    
    match connectfour.prompt(
            """
Please enter a number from 1-3
To exit, enter 0
    1. Get your cake
    2. Hear a joke
    3. Play connect four
            """,
            lambda x: x>=0 and x<=3,
            response_type=int):

        case 0:
            break
        case 1:
            Image.open('./cake.webp').show()
            time.sleep(3)
        case 2:
            print(pyjokes.get_joke())
            time.sleep(3)
        case 3:
            connectfour.play_game()
            time.sleep(3)

