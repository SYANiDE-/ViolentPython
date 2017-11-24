#!/usr/bin/env python2
import re

temp=[]
temp = '{"success":true,"cdma":false,"gsm":false,"wifi":false,"addresses":[],"results":[{"trilat":25.04802132,"trilong":121.56586456,"ssid":"Powerful-7F","qos":0,"transid":"20170404-00371","firsttime":"2017-04-05T05:41:51.000Z","lasttime":"2017-04-04T15:17:53.000Z","lastupdt":"2017-04-04T15:18:03.000Z","housenumber":null,"road":null,"city":null,"region":null,"country":null,"netid":"00:11:A3:1C:39:CE","name":null,"type":"infra","comment":null,"wep":"2","channel":1,"bcninterval":0,"freenet":"?","dhcp":"?","paynet":"?","userfound":null,"locationData":[{"alt":44,"accuracy":11.0,"lastupdt":"2017-04-04T15:17:53.000Z","latitude":25.04802132,"longitude":121.56586456,"month":"201704","ssid":"Powerful-7F","time":"2017-04-05T05:41:51.000Z","signal":-80.0,"name":null,"netId":"75750980046","noise":0.0,"snr":0.0,"wep":"2","encryptionValue":"WPA2"}],"encryption":"wpa2"}]}'
lat = ""
lon = ""
rlat = re.findall(r'latitude.*,', temp)[0].split(":")[1].split(",")[0]
rlon = re.findall(r'longitude.*,', temp)[0].split(":")[1].split(",")[0]
print rlat
print rlon


