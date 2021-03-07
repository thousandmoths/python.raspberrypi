import json
import subprocess
import time
import socket
import psutil
import requests
# Import Blinka
from board import SCL, SDA
import busio
import adafruit_ssd1306

# Import Python Imaging Library
from PIL import Image, ImageDraw, ImageFont

WIDTH = 128
HEIGHT = 64
BORDER = 0
DURATION = 5

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)

# Load fonts.
title_font = ImageFont.truetype("Ubuntu-Bold.ttf", 17)
font = ImageFont.truetype("Ubuntu-Bold.ttf", 20)
small_font = ImageFont.truetype("Ubuntu-Medium.ttf", 18)

# Define an image using 1-bit color
image = Image.new('1', (oled.width, oled.height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

def get_cpu_temp():
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    cpu_temp = '{:.2f}'.format( float(cpu)/1000 ) + "° C"
    return cpu_temp

def display_cpu_temp():
    clear_display()
    for i in range(DURATION):
        title = "CPU TEMP"
        (font_width, font_height) = font.getsize(title)
        draw.text(((oled.width//2 - font_width//2), 0), 
        title, font=title_font, fill=255)
        # Clear the dynamic part of the display
        draw.rectangle((0, 16, oled.width, oled.height), outline=0, fill=0)
        text = get_cpu_temp()
        (font_width, font_height) = font.getsize(text)
        draw.text((oled.width//2 - font_width//2, oled.height//2 - font_height//2), 
            text, font=font, fill=255)
        # Display image
        oled.image(image)
        oled.show()
        time.sleep(1)
    return

def get_cpu_speed(): # get the CPU speed 
    tmp1 = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    freq = tmp1.read
    cpu_speed = ('%u MHz' % (int(freq()) / 1000))
    return cpu_speed

def display_cpu_speed():
    clear_display()
    for i in range(DURATION):
        title = "CPU SPEED"
        (font_width, font_height) = font.getsize(title)
        draw.text(((oled.width//2 - font_width//2), 0), 
        title, font=title_font, fill=255)
        # Clear the dynamic part of the display 
        draw.rectangle((0, 16, oled.width, oled.height), outline=0, fill=0)
        # Define the content to be displayed
        text = get_cpu_speed()
        (font_width, font_height) = font.getsize(text)
        draw.text((oled.width//2 - font_width//2, oled.height//2 - font_height//2), 
            text, font=font, fill=255)
        # Draw the display
        oled.image(image)
        oled.show()
        time.sleep(1)
    return

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

def display_ip_address():
    clear_display()
    for i in range(DURATION):
        title = "IP"
        (font_width, font_height) = font.getsize(title)
        draw.text(((oled.width//2 - font_width//2), 0), 
        title, font=title_font, fill=255)
        # Clear the dynamic part of the display
        draw.rectangle((0, 16, oled.width, oled.height), outline=0, fill=0)
        ip = get_ip_address()
        (font_width, font_height) = font.getsize(ip)
        draw.text((5, oled.height//2 - font_height//2), 
            ip, font=small_font, fill=255)
        host_name = (socket.gethostname())
        (font_width, font_height) = font.getsize(host_name)
        draw.text((oled.width//2 - font_width//2, 40), 
            host_name, font=small_font, fill=255)
        # Display image
        oled.image(image)
        oled.show()
        time.sleep(1)
    return

def clear_display():
    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
    # Draw a smaller inner rectangle
    draw.rectangle((BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1), outline=0, fill=0)

while True:
    display_cpu_temp()
    display_cpu_speed()
    display_ip_address()