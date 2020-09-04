from uiflow import *
from m5stack import *
from m5ui import *

import urequests
import wifiCfg

def set_status(status):
 	status_bar.setBgColor(status_colors[status])
 	status_bar.setBorderColor(status_colors[status])

def post_to_server(data):
	try:
		url = server_url+"/"+cfgRead('data_schema')['title']+"/"+cfgRead('uid')
		print("posting to ", url)
		response = urequests.request(
			method='POST',
			json=data,
			url=url
		)
		return response
	except:
		pass

STATUS_OK = 0
STATUS_ERROR = 1

status_colors ={
	STATUS_OK: 0x00FF00,
	STATUS_ERROR: 0xFF0000
}

lcd.clear(lcd.BLACK)

data_schema = cfgRead('data_schema')
server_url = cfgRead('server_url')

status_bar = M5Rect(0, 0, 80, 20, 0x000000, 0x000000)

wifi_config = cfgRead('wifi')

if wifi_config is not None:
	try:
		wifiCfg.doConnect(
			wifi_config['ssid'],
			wifi_config['password']
		)
		set_status(STATUS_OK)
	except:
		set_status(STATUS_ERROR)

if data_schema is not None:
	if 'default' in data_schema:
		response = post_to_server(data_schema['default'])
		if response is None:
			set_status(STATUS_ERROR)
			print("Posting to server failed")
		else:
			if response.json() == True:
				set_status(STATUS_OK)
				print("Posting to server success")
			else:
				print("Server response error")
				set_status(STATUS_ERROR)
else:
	set_status(STATUS_ERROR)
	print("Data schema not found in config")