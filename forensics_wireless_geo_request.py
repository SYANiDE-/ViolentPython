import os, sys, mechanize, urllib, re, getpass, json

def wigle_query(u, p, mac, net):
	a = mechanize.Browser()
	a.open('https://wigle.net')
	reqData = urllib.urlencode({
		'credential_0':u, 
		'credential_1':p
	})
	resp = a.open('https://api.wigle.net/api/v2/login', reqData).read()
	params = {}
	params['netid'] = mac
        params['ssid'] = net
	reqParams = urllib.urlencode(params)
	resp_req = 'https://api.wigle.net/api/v2/network/detail'
	# resp = a.open(resp_req, reqParams).read()  # POST method
	resp = a.open(resp_req+ '?%s' + reqParams).read() # GET method
	print(resp)
	mapLat = 'N/A'
	mapLon = 'N/A'
	rLat = re.findall(r'latitude.*,', resp)
	rLon = re.findall(r'longitude.*,', resp)
	if rLat:
            mapLat = rLat[0].split(':')[1].split(',')[0]
	if rLon:
	    mapLon = rLon[0].split(':')[1].split(',')[0]
        print('[-] Mac: ' +mac+ ', Net: ' +net+ ', Lat: ' +mapLat+ ', Lon: ' +mapLon)





u = 'sgamma'
p = getpass.getpass()
mac = "00:11:A3:1C:39:CE"
net = "Powerful-7F"
print("[+] " +mac+ " " +net)
wigle_query(u, p, mac, net)

