from beem import Steem
from beem.comment import Comment
from datetime import datetime, timedelta, timezone
from dateutil import parser
import os
import time
print(time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.localtime()),flush=True) 

import dbadapter
conn= dbadapter.get_conn()
cursor = conn.cursor()
def getdict_query(query):	
	colname = [ d[0] for d in query.description ]
	result_list = [ dict(zip(colname, r)) for r in query.fetchall() ]
	return result_list
	
username = dbadapter.get_user()
password = dbadapter.get_pw()

jetzt = datetime.now(timezone.utc).timestamp()
cursor.execute("SELECT * FROM s_remindme WHERE finished =0 and tmstmp <%s",[jetzt,])
ret = getdict_query(cursor)
if ret:
	s = Steem()
	steem.wallet.unlock(password)
	for pst in ret:
		print(pst,jetzt)
		po = Comment("@"+pst['username']+'/'+pst['permlink'],s)
		body='You wanted to be reminded'
		returncode = po.reply(body=body,author=username)
		print(returncode)
		cursor.execute("UPDATE s_remindme SET finished =1 WHERE id =%s",[pst['id'],])
		conn.commit()
		try:
			cpermlink = returncode['operations'][0][1]['permlink']
			cauthor = 'remindme.bot'
			cdate = str(datetime.utcnow())
			cursor.execute("INSERT INTO comments_to_upvote (author, permlink,post_date, finished) VALUES (%s,%s,%s,%s)",[cauthor, cpermlink,cdate,0])
			conn.commit()
		except Exception as e:
			print(e)
