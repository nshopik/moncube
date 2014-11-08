import json
from time import localtime, time, strftime, timezone
from collections import OrderedDict
import codecs

tz = str.format('{0:+06.2f}', -float(timezone) / 3600).replace('.', ':')

def jsonwrite(data, logfile):
	logfile = logfile + '.log'
	data['Timestamp'] = int(time())
	od = OrderedDict(data)
	text = json.dumps(od, ensure_ascii=False, separators=(',',':')) #compact
#	print (text)
	f = codecs.open(logfile, 'a', encoding='utf8')
	f.write (text + "\r\n")
	f.close()