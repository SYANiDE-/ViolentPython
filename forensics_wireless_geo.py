import os, sys, _winreg, mechanize, urllib, re, getpass
## Require Windows version of Python for _winreg lib.


notes=("""
## Can't really do the same thing as the book, using wigle.net:
1.  The uris "/gps/gps/main/login" and  "/gps/gps/main/confirmquery/" are 302 and 404 respectively.
2.  API now, and JSON output instead of HTML (or whatever it was in the book)

HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged
  ProfileGuid
  Description
  Source
  DnsSuffix
  FirstNetwork    (network name)
  DefaultGatewayMac    (network mac)
""")


def mac_from_bytes(v):
        addy = ""
        for b in v:
                addy+= ("%02x " % ord(b))
        addy = addy.strip(" ").replace(" ", ":")[0:17]
	return addy


def gather(u, p):
	target_keys = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"
	key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, target_keys)
	for i in range(5):
		try:
			guid = _winreg.EnumKey(key, i)
			netKey = _winreg.OpenKey(key, str(guid))
			(n, name, t) = _winreg.EnumValue(netKey, 4)
			(n, addr, t) = _winreg.EnumValue(netKey, 5)
			mac = mac_from_bytes(addr)
			net = str(name)
			print("[+] " +mac+ " " +net)
			wigle_query(u, p, mac, net)
			_winreg.CloseKey(netKey)
		except Exception, e:
			print(str(e))


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
		mapLat = rLat[0].split(":")[1].split(",")[0]
	if rLon:
		mapLon = rLon[0].split(":")[1].split(",")[0]
	print('[-] Mac: ' +mac+ ', Net: ' +net+ ', Lat: ' +mapLat+ ', Lon: ' +mapLon)



def main():
	u = 'sgamma'
	p = getpass.getpass()
	gather(u, p)



if __name__=="__main__":
	main()



