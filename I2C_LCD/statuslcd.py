import I2C_LCD_driver
import time
import socket
import psutil

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()
duration = 10
wait = 0.5

def get_cpu_temp(): # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    cpu_temp = '{:.2f}'.format( float(cpu)/1000 ) + chr(223) + 'C'
    return cpu_temp

def get_cpu_speed(): # get the CPU speed 
    tmp1 = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    freq = tmp1.read
    cpu_speed = ('%u MHz' % (int(freq()) / 1000))
    return cpu_speed

def get_cpu_load(): # use psutil to get the current load
    cpu_load = "%s" %psutil.cpu_percent() + "%"
    return cpu_load

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

while True:
    for i in range(duration):
        mylcd.lcd_display_string("Speed: " + get_cpu_speed() + " ", 1)
        mylcd.lcd_display_string("Temp: " + get_cpu_temp(), 2)
        time.sleep(wait)
    mylcd.lcd_clear()

    for i in range(duration):
        mylcd.lcd_display_string("Load: " + get_cpu_load(), 1)
        mylcd.lcd_display_string("Temp: " + get_cpu_temp(), 2)
        time.sleep(wait)
    mylcd.lcd_clear()

    for i in range(duration):
        mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 1)
        mylcd.lcd_display_string("Date: %s" %time.strftime("%d/%m/%Y"), 2)
        time.sleep(wait)
    mylcd.lcd_clear()
    
    for i in range(duration):
        mylcd.lcd_display_string(socket.gethostname())
        mylcd.lcd_display_string("IP:" + get_ip_address(), 2)
        time.sleep(wait)
    mylcd.lcd_clear()
    