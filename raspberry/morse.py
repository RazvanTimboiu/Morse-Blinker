import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import RPi.GPIO as GPIO
from time import sleep
import json
import paho.mqtt.client as mqtt

from config import CLIENT_USERNAME, CLIENT_PASSWORD, CLIENT_CODE

# Display size
WIDTH = 128
HEIGHT = 64
BORDER = 5

led_pin = 4
GPIO.setup(led_pin, GPIO.OUT) 

morse = {"A": ".-",
         "B": "-...",
         "C": "-.-.",
         "D": "-..",
         "E": ".",
         "F": "..-.",
         "G": "--.",
         "H": "....",
         "I": "..",
         "J": ".---",
         "K": "-.-",
         "L": ".-..",
         "M": "--",
         "N": "-.",
         "O": "---",
         "P": ".--.",
         "Q": "--.-",
         "R": ".-.",
         "S": "...",
         "T": "-",
         "U": "..-",
         "V": "...-",
         "W": ".--",
         "X": "-..-",
         "Y": "-.--",
         "Z": "--.."
    }




def show_letter(text):

    # Use for I2C.
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

    # Clear display.
    oled.fill(0)
    oled.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    # Draw a smaller inner rectangle
    draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
    )

    # Load a true type font.
    font = ImageFont.truetype("ZenDots-Regular.ttf", 16)


    # Draw Some Text
    (font_width, font_height) = font.getsize(text)

    draw.text(
    (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
    text,
    font=font,
    fill=255,
    )

    # Display image
    oled.image(image)
    oled.show()
    
def blink_dash():
    GPIO.output(led_pin, GPIO.HIGH)
    sleep(1)
    GPIO.output(led_pin, GPIO.LOW)
    sleep(0.5)
    
    

def blink_dot():
    GPIO.output(led_pin, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(led_pin, GPIO.LOW)
    sleep(0.5)
    

def blink_letter(letter):
    for c in morse[letter]:
        if c == ".":
            blink_dot()
        else :
            blink_dash()
    

def display_message(word):
    for letter in word:
        if letter in morse:
            show_letter(letter)
            blink_letter(letter)
            sleep(0.3)
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
    oled.fill(0)
    
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))
        
def on_message(client, userdata, msg):
    if msg.topic == "morse":
        msg = msg.payload.decode("utf-8")
        print(msg)
        display_message(msg)
        
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# enable TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set(CLIENT_USERNAME, CLIENT_PASSWORD)

# connect to HiveMQ Cloud on port 8883
client.connect(CLIENT_CODE, 8883)

# subscribe to the "morse" topic
client.subscribe("morse")

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_start()

try:
    while True:
        continue
finally:
    GPIO.cleanup()
    