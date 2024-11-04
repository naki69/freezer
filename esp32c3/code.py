import machine, onewire, ds18x20, time
import network, ntptime
import urequests, ujson

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Down', '69696969')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ipconfig('addr4'))
    
def set_time():
    rtc = machine.RTC()
    ntptime.settime() # set the rtc datetime from the remote server
    rtc.datetime()    # get the date and time in UTC
       
def send_data(mydata):
    url = 'http://192.168.0.188:8080'
    mydata = [mydata,]
    x = urequests.post(url, json=mydata)
    if x.status_code == 200:
        print("Done")

def get_data(ds_sensor, roms):
    buf = dict()
    ds_sensor.convert_temp()
    time.sleep_ms(1000)
    buf['time'] = time.time()
    for i,rom in enumerate(roms):
        k = "temp" + str(i+1)
        buf[k] = float(ds_sensor.read_temp(rom))
    return (buf)

def main():
    do_connect()
    set_time()
    ds_pin = machine.Pin(10)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

    roms = ds_sensor.scan()
    data = list()
    while True:            
        for i in range(10):
            print(i)
            data.append(get_data(ds_sensor, roms))
            
        send_data(data)

        
if __name__ == "__main__":
    main()
