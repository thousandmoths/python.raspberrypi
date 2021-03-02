import I2C_LCD_driver
import time
from datetime import datetime, timedelta
import socket
import fcntl
import struct
import psutil

mylcd = I2C_LCD_driver.lcd()
duration = 5
wait = 1

def get_ip_address(ifname): # get IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, 
        struct.pack('256s', ifname[:15])
    )[20:24])

def get_cpu_temp(): # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_cpu_speed(): # get the CPU speed 
    tmp1 = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    freq = tmp1.read
    return ('%u MHz' % (int(freq()) / 1000))

def get_time_now(): # get the current time
    time_now = "Time: %s" %time.strftime("%H:%M:%S")
    return time_now

def get_date_now(): # get the current date
    date_now = "Date: %s" %time.strftime("%d/%m/%Y")
    return date_now

def get_cpu_load(): # use psutil to get the current load
    cpu_load = "%s" %psutil.cpu_percent()
    return cpu_load

def display_ip_address(): # display the IP
    end_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < end_time:
        mylcd.lcd_display_string("IP Address:", 1)
        mylcd.lcd_display_string(get_ip_address('wlan0'), 2)

def display_time(): # display the time
    end_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < end_time:
        mylcd.lcd_display_string(get_time_now(), 1)
        mylcd.lcd_display_string(get_date_now(), 2)

def display_cpu_temp(): # display the CPU temperature
    end_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < end_time:
        mylcd.lcd_display_string("CPU Temp: ", 1)
        mylcd.lcd_display_string(get_cpu_temp(), 2)
        time.sleep(wait)

def display_cpu_load(): # display the CPU load
    end_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < end_time:
        mylcd.lcd_display_string("CPU Load:", 1)
        mylcd.lcd_display_string(get_cpu_load() + " % ",2)
        time.sleep(wait)

def display_cpu_speed(): # display the CPU speed
    end_time = datetime.now() + timedelta(seconds=duration)
    while datetime.now() < end_time:
        mylcd.lcd_display_string("CPU Speed: ", 1)
        mylcd.lcd_display_string(get_cpu_speed() + " ", 2)
        time.sleep(wait)

while True:
    display_ip_address()
    mylcd.lcd_clear()
    display_time()
    mylcd.lcd_clear()
    display_cpu_temp()
    mylcd.lcd_clear()
    display_cpu_load()
    mylcd.lcd_clear()
    display_cpu_speed()
    mylcd.lcd_clear()
