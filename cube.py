from win32gui import GetWindowText, GetForegroundWindow
from win32process import GetWindowThreadProcessId
import win32api
import psutil
from time import sleep, localtime, time, strftime
import json

# local import
import jsonwrite as log
TotalIdle = 0
logfile = strftime("%Y-%m-%d", localtime())
ActivePIDs = []

print ('Cube Version 0.1\r\n', logfile + '.log')
def getActiveWindow(idle):
	hwnd = GetForegroundWindow()
	if hwnd == 0:
		sleep (0.1)
		return getActiveWindow(getIdleTime())
	curw = GetWindowText(hwnd)
	wpid = GetWindowThreadProcessId(hwnd)
	p = psutil.Process(wpid[1])
	pexe = p.exe()
	pctime = p.create_time()
	global TotalIdle
	sleep(1)
	print (getProcessHandle(wpid[1]))
	if idle > getIdleTime():
		TotalIdle = TotalIdle + idle
	if curw != GetWindowText(GetForegroundWindow()):
		data = {}
		data['PID'] = wpid[1]
		data['EXE'] = pexe
		data['CTime'] = int(pctime)
		data['WTitle'] = curw
		data['idleTimer'] = TotalIdle
		log.jsonwrite(data, logfile)
		TotalIdle = 0

def getProcessHandle(wpid):
	handle = win32api.OpenProcess(0x10000410, False, wpid)
	return handle

def getIdleTime():
	millis = win32api.GetTickCount() - win32api.GetLastInputInfo()
	return millis / 1000.0

while True:
	getActiveWindow(getIdleTime())