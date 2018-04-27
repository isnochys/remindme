from beem import Steem
from beem.account import Account
from datetime import datetime, timedelta
from dateutil import parser
import os
import re
import time
print(time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime()),flush=True) 

import dbadapter
conn = dbadapter.get_conn()
cursor = conn.cursor()
query = '#remindme: '
username = 'isnochys'


def get_timedelta(ziffer,windo):
	if windo =='d':
		tmd = timedelta(days=int(ziffer))
	elif windo =='m':
		tmd = timedelta(minutes=int(ziffer))
	elif windo =='w':
		tmd = timedelta(weeks=int(ziffer))
	elif windo =='h':
		tmd = timedelta(hours=int(ziffer))
	
	return tmd
	
s = Steem()
a = Account(username,s)
hrl = a.history_reverse(only_ops=['comment'])
def getdict_query(query):	
	colname = [ d[0] for d in query.description ]
	result_list = [ dict(zip(colname, r)) for r in query.fetchall() ]
	return result_list
	
last_block =0
cursor.execute("SELECT * FROM s_remindme ORDER BY block DESC Limit 1")
ret = getdict_query(cursor)
if ret:
	last_block = ret[0]['block']
for op in hrl:
	if last_block>=op['block']:
		break
	if op['author'] == username and query in op['body']:
		timestamp = parser.parse(op['timestamp']+' UTC')
		print(op)
		print(op['body'].split(query)[1].split())
		deltapl = op['body'].split(query)[1].split()
		deltap = deltapl[0]
		datum =''
		if deltap.startswith('+'):
			pattern = re.compile(r'(?:#remindme: )?(([+-])(\d+)(\w))\s?', re.IGNORECASE)
			matchl = pattern.findall(deltap)
			datum = timestamp
			for match in matchl:
				if match[1]='-':
					datum -= get_timedelta(match[2],match[3])
				elif match[1]=='+':
					datum += get_timedelta(match[2],match[3])
		else:
			try:
				datum = parser.parse(' '.join(deltapl))
			except Exception as e:
				print(e)
		if datum:
			tmpstmp = datum.timestamp()
			cursor.execute("INSERT INTO s_remindme (username,permlink,datum,finished,block,tmstmp) VALUES (%s,%s,%s,%s,%s,%s)",[username,op['permlink'],str(datum),0,op['block'],tmpstmp])
			conn.commit()

	
