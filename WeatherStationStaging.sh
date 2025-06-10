#! /bin/bash

echo "Stage the setup of the Weather Station"
sudo apt-get update
sudo apt-get -y upgrade 
sudo apt-get install -y git cmake build-essential curl libcurl4-openssl-dev libssl-dev uuid-dev
sudo apt-get install -y nodejs npm vim
sudo npm install -y -g npm
sudo npm cache clean -f
sudo npm install -y -g n
sudo n stable
sudo apt-get install -y python3-full
sudo python3 -m pip config set global.break-system-packages true
sudo pip3 install azure-iot-device  
sudo pip3 install azure-iot-hub
sudo apt-get install -y i2c-tools build-essential
sudo pip3 install adafruit-circuitpython-bmp280
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
sudo python ~/Adafruit_Python_DHT/setup.py install
cd Adafruit_Python_DHT
sudo python setup.py install
echo "############################################"
echo "##### Weather Station Staging Complete #####"
echo "############################################"
sudo reboot