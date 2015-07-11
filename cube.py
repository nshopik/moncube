from win32gui import GetWindowText, GetForegroundWindow
from win32process import GetWindowThreadProcessId
import win32api
import psutil
from time import sleep, localtime, time, strftime
from collections import OrderedDict

# local import
import jsonwrite as log
TotalIdle = 0
logfile = strftime("%Y-%m-%d", localtime())
LastWin = []
ActiveTime = int(time())
pid = 0

print ('Cube Version 0.2.1\r\n', logfile + '.log')
def getActiveWindow():
	hwnd = GetForegroundWindow()
	if hwnd == 0:
		sleep (0.1)
		return getActiveWindow()
	curw = GetWindowText(hwnd)
	wpid = GetWindowThreadProcessId(hwnd)
	return curw, wpid[1]

def getProcessHandle(pid):
	handle = win32api.OpenProcess(0x10000410, False, pid)
	return handle

def getIdleTime():
	millis = win32api.GetTickCount() - win32api.GetLastInputInfo()
	return millis / 1000.0

while True:
	window = getActiveWindow()
	if pid == 0:
		pid = window[1]
		try:
			p = psutil.Process(pid)
			exe = p.name()
			ctime = int(p.create_time())
		except:
			exe = None
			ctime = None
	if not LastWin:
		LastWin = window
	if LastWin[0] != GetWindowText(GetForegroundWindow()):
		data = OrderedDict()
		data['PID'] = pid
		data['EXE'] = exe
		data['CTime'] = ctime
		data['WTitle'] = LastWin[0]
		data['idleTime'] = int(TotalIdle)
		data['ActiveTime'] = int(time()) - ActiveTime
		log.jsonwrite(data, logfile)
		TotalIdle = 0
		pid = 0
		LastWin = []
		ActiveTime = int(time())
	else:
		idle = getIdleTime()
		sleep(1)
		if idle > getIdleTime():
			TotalIdle = TotalIdle + idle
