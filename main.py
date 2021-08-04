from m5stack import *
from m5stack_ui import *
from uiflow import *
import wifiCfg
import urequests
import time
import json

import unit

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xffffff)
Watering_1 = unit.get(unit.WATERING, (26,35))
env2_1 = unit.get(unit.ENV2, unit.PORTA)
light_1 = unit.get(unit.LIGHT, (25,36))


status = None
lightlvl = None
soilmoisture = None
json_data = None
temperature = None
humidity = None
pressure = None
DataMap = None

wifiCfg.autoConnect(lcdShow=True)
wifiCfg.reconnect()
image0 = M5Img("res/waylay.png", x=110, y=207, parent=None)
moisture = M5Label('Text', x=140, y=72, color=0x30b719, font=FONT_MONT_20, parent=None)
light = M5Label('Text', x=19, y=72, color=0x30b719, font=FONT_MONT_20, parent=None)
temp = M5Label('Text', x=19, y=170, color=0x30b719, font=FONT_MONT_20, parent=None)
image3 = M5Img("res/temp.png", x=19, y=81, parent=None)
h = M5Label('Text', x=132, y=170, color=0x30b719, font=FONT_MONT_20, parent=None)
image4 = M5Img("res/temp.png", x=10, y=80, parent=None)
p = M5Label('Text', x=239, y=170, color=0x30b719, font=FONT_MONT_20, parent=None)
ps = M5Label('Waiting', x=19, y=217, color=0x30b719, font=FONT_MONT_14, parent=None)
HttpStatus = M5Label('Status', x=249, y=217, color=0x30b719, font=FONT_MONT_14, parent=None)
image1 = M5Img("res/1-light.png", x=29, y=20, parent=None)
image2 = M5Img("res/2-soilhum.png", x=140, y=20, parent=None)
image5 = M5Img("res/3-pump.png", x=251, y=20, parent=None)
image6 = M5Img("res/4-temp.png", x=29, y=124, parent=None)
image7 = M5Img("res/5-airhum.png", x=140, y=124, parent=None)
image8 = M5Img("res/6-pressure.png", x=251, y=124, parent=None)
PumpStat = M5Label('Text', x=227, y=72, color=0x30b719, font=FONT_MONT_20, parent=None)


# Describe this function...
def SendPOST():
  global status, lightlvl, soilmoisture, json_data, temperature, humidity, pressure, DataMap
  status = 'No StatusCode'
  try:
    req = urequests.request(method='POST', url='Replace_With_Your_Webscript_Address',data=json_data, headers={'Content-Type':'application/json'})
    ps.set_text_color(0x006600)
    wait(5)
    status = req.status_code
    ps.set_text('Data sent')
  except:
    ps.set_text_color(0x990000)
    wait(5)
    ps.set_text('Not sent')
  wait(5)
  HttpStatus.set_text(str(status))

# Describe this function...
def Enviro():
  global status, lightlvl, soilmoisture, json_data, temperature, humidity, pressure, DataMap
  lightlvl = light_1.analogValue
  soilmoisture = Watering_1.get_adc_value()
  temperature = env2_1.temperature
  humidity = env2_1.humidity
  pressure = env2_1.pressure
  DataMap = {'Soil Moisture':soilmoisture,'Temperature':temperature,'Humidity':humidity,'Pressure':pressure,'Light':lightlvl}
  json_data = json.dumps(DataMap)
  light.set_text(str(lightlvl))
  moisture.set_text(str(soilmoisture))
  temp.set_text(str(temperature))
  h.set_text(str(humidity))
  p.set_text(str(pressure))

# Describe this function...
def WaterPlant():
  global status, lightlvl, soilmoisture, json_data, temperature, humidity, pressure, DataMap
  for count in range(6):
    if (Watering_1.get_adc_value()) < 1500:
      PumpStat.set_text('Watering Plants')
      Watering_1.set_pump_status(1)
    else:
      PumpStat.set_text('Waiting')
      Watering_1.set_pump_status(0)
    wait(2)
  PumpStat.set_text('Waiting')
  Watering_1.set_pump_status(0)



import custom.urequests as urequests
while True:
  if wifiCfg.wlan_sta.isconnected():
    Enviro()
    WaterPlant()
    SendPOST()
    wait(10)
  else:
    wait(1)
    lcd.print('reconnecting', 0, 30, 0x33ff33)
    wait(1)
  wait_ms(2)

