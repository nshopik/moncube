import json
from time import time
from collections import OrderedDict
import codecs

def jsonwrite(data, logfile):
	logfile = logfile + '.log'
	data['Timestamp'] = int(time())
	od = OrderedDict(data)
	text = json.dumps(od, ensure_ascii=False, separators=(',',':')) #compact
	f = codecs.open(logfile, 'a', encoding='utf8')
	f.write (text + "\r\n")
	f.close()