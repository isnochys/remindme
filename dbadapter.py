import configparser
config = configparser.ConfigParser()


def get_conn():

	ret = config.read('settings.ini')

	if not ret:
		config.read('settings-sample.ini')

	mydb = config['settings']['adapter']
	if mydb == 'mysql':
		import MySQLdb as mdb
		host = config[mydb]['host']
		user = config[mydb]['user']
		pw = config[mydb]['pw']
		thisdb = config[mydb]['name']
		conn = mdb.connect(host, user, pw, thisdb,use_unicode=True, charset="utf8mb4")
		conn1 = conn
		conn1.set_character_set('utf8mb4')
		cursor1 = conn1.cursor()
		cursor1.execute('SET NAMES utf8mb4;')
		cursor1.execute('SET CHARACTER SET utf8mb4;')
		cursor1.execute('SET character_set_connection=utf8mb4;')
	else:
		import sqlite3
		thisdb = config[mydb]['name']
		conn = sqlite3.connect(thisdb)
		
	return conn

def get_pw():

	ret = config.read('settings.ini')

	if not ret:
		config.read('settings-sample.ini')

	password = config['settings']['password']
	return password
def get_user():
	ret = config.read('settings.ini')

	if not ret:
		config.read('settings-sample.ini')

	username = config['settings']['username']
	return username
