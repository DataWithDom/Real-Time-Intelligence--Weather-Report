
import Adafruit_DHT
import time
import os
from azure.iot.device import IoTHubDeviceClient, Message  
from configWeatherStation import *
#import Adafruit_BMP
#import smbus
#import RPi.GPIO as GPIO
import board
import adafruit_bmp280

time.sleep(60)

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c,address=0x76)

# change this to match the location's pressure (hPa) at sea level
bmp280.sea_level_pressure = 1013.25


DeviceId = DeviceName
#pressure = 1000
sensor = 11 #Adafruit_DHT.DHT22
pin = 17

#Temperature Gauge Functions
def setup():
	global ds18b20
	for i in os.listdir('/sys/bus/w1/devices'):
		if i != 'w1_bus_master1':
			ds18b20 = i #Finds the unique serial number for the Temperature Gauge

def read():
#	global ds18b20
	location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave' #Sets the location for the temperature gauge
	tfile = open(location,'r') #Opens file in the location
	text = tfile.read() #Reads the file
	tfile.close() #Closes the file
	secondline = text.split("\n")[1] #Parses out data
	temperaturedata = secondline.split(" ")[9] #Pulls the current temperature from the file
	temperature = float(temperaturedata[2:]) #Converts to a float number
	temperature = temperature / 1000 #Converts value to Celsius 
	return temperature #Returns value for the function


setup() #Calls setup function to find serial number for the ds18b20 temperature sensor

CONNECTION_STRING = DeviceConnectionString
MSG_SND = '{{"location: {location} "temperature": {temperature},"humidity": {humidity}}}'  
while True:
    def iothub_client_init():  
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)  
        return client  
    def send_Weather_Report():  
        try:  
            client = iothub_client_init()  
            print ( "Sending data to IoT Hub, press Ctrl-C to exit" )  
            while True:  
                humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                pressure = bmp280.pressure
                tempsensor = read() #Reads the temperature sensor and stores to tempsensor
                WeatherData = {'DeviceID':DeviceId, #Device ID for reporting to the IoT Hub
                    'Humidity':float(humidity), #Print out Humidity
                    'Temperature':tempsensor, #Print out Temperature
                    'Barometer':pressure #Print out Barometer Reading
                    #'BarometerChange':barochange #Placeholder for barometer change rating
                    } 
                #msg_txt_formatted = MSG_SND.format(location=location, temperature=temperature, humidity=humidity)  
                msg_txt_formatted = str(WeatherData) #Converts values found above into a string
                message = Message(bytearray(msg_txt_formatted, 'utf8')) #Formats into utf8 for the IoT Hub
                #message = Message(msg_txt_formatted)  
                print( "Sending message: {}".format(message) )  
                client.send_message(message)  
                print ( "Message successfully sent" )  
                time.sleep(10)  
        except KeyboardInterrupt:  
            print ( "IoTHubClient stopped" )  
    if __name__ == '__main__':  
        print ( "Press Ctrl-C to exit" )  
        send_Weather_Report()