import os, _winreg



reg = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\"
dirs = ['c:\\Recycler\\', 'c:\\Recycled\\', 'c:\\$Recycle.bin\\']


def which_win_ver():
	for rbin in dirs:
		if os.path.isdir(rbin):
			return rbin
	return None


def enum_targets(dir):
	sids = []
	regtargets = []
	dirtargets = []
	for ghost in os.listdir(dir):
		sids.append(ghost)
		regtargets.append("HKEY_LOCAL_MACHINE\\" + reg + ghost)
		dirtargets.append(dir + ghost)
	for (x,y,z) in zip(sids, regtargets, dirtargets):
		user = sid2user(x)
		files = os.listdir(z)
		print("\n[!] Found deleted files for user %s:%s in %s:" % (user, x.split("-")[-1], z))
		for f in files:
			print("[!] %s:%s" % (user, f))
			


def sid2user(sid):
	try:
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, reg +sid)
		(value, type) = _winreg.QueryValueEx(key, 'ProfileImagePath')
		print(value, type)
		user = value.split('\\')[-1]
		return user
	except:
		return sid	


if __name__=="__main__":
	enum_targets(which_win_ver())
