import I2C_LCD_driver
import time
import psutil

mylcd = I2C_LCD_driver.lcd()
duration = 4
wait = 1
mylcd.lcd_clear()

def get_cpu_temp(): # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_cpu_speed(): # get the CPU speed 
    tmp1 = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    freq = tmp1.read
    return ('%u MHz' % (int(freq()) / 1000))

def get_cpu_load(): # use psutil to get the current load
    cpu_load = "%s" %psutil.cpu_percent()
    return cpu_load

while True:
    counter = 0
    mylcd.lcd_clear()
    while counter < duration:
        mylcd.lcd_display_string("CPU Speed: ", 1)
        mylcd.lcd_display_string(get_cpu_speed() + " ", 2)
        time.sleep(wait)
        counter += 1
    counter = 0
    mylcd.lcd_clear()
    while counter < duration:
        mylcd.lcd_display_string("CPU Load:", 1)
        mylcd.lcd_display_string(get_cpu_load() + " % ",2)
        time.sleep(wait)
        counter += 1
    counter = 0
    mylcd.lcd_clear()
    while counter < duration:
        mylcd.lcd_display_string("CPU Temp: ", 1)
        mylcd.lcd_display_string(get_cpu_temp(), 2)
        time.sleep(wait)
        counter += 1
    counter = 0
    mylcd.lcd_clear()
    while counter < duration:
        mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 1)
        mylcd.lcd_display_string("Date: %s" %time.strftime("%d/%m/%Y"), 2)
        time.sleep(wait)
        counter += 1
    counter = 0
    mylcd.lcd_clear()

