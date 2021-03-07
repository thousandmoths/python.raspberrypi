from board import SCL, SDA
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
WIDTH = 128
HEIGHT = 64
i2c = busio.I2C(SCL, SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)
image = Image.new('1', (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
oled.image(image)
oled.show()