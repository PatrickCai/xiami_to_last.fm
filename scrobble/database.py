#! /usr/bin/env python
# -- encoding:utf - 8 --
import sys
import re
import os
import MySQLdb
import sae.const
import logging
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

def start():
	if 'SERVER_SOFTWARE' not in os.environ:
		host = 'localhost'
		user = 'root'
		passwd = ''
		db = 'scrobble'
		port = 3306
	else:
		host = sae.const.MYSQL_HOST 
		user = sae.const.MYSQL_USER 
		passwd = sae.const.MYSQL_PASS 
		db = sae.const.MYSQL_DB
		port = int(sae.const.MYSQL_PORT)

	conn = MySQLdb.connect(host=host, user=user, passwd=passwd,db=db, port=port)
	cur = conn.cursor()
	return conn, cur


def end(conn,cur):
	cur.close()
	conn.close()

def get_last_loved_song(user_ID):
	(conn, cur) = start()
	values = [user_ID]
	cur.execute('SELECT * FROM users WHERE users_ID=%s', values)
	result = cur.fetchone()
	end(conn, cur)
	last_loved_song = result[5]
	return last_loved_song

def is_user_exist(user_ID):
	(conn, cur) = start()
	values = [user_ID]
	cur.execute('SELECT * FROM users WHERE users_ID=%s', values)
	result = cur.fetchone()
	end(conn, cur)
	should_continue = not bool(result)
	return should_continue

def insert_user(user_ID, token, record_time):
	(conn, cur) = start()
	start_times = 0
	now_time = datetime.now()
	last_loved_song = "None"
	values = [user_ID, token, record_time, start_times, now_time, last_loved_song]
	cur.execute('insert into users values(%s, %s, %s, %s, %s, %s)',
					values)
	conn.commit()
	end(conn, cur)

def modify_last_loved_song(user_ID, song_ID):
	'''
	Modify user's last loved song
	# Parameters:
	* user_ID: user's ID
	* song_ID the last song's ID
	'''
	song_ID = str(song_ID)#The database type is string
	user_ID = int(user_ID)
	(conn, cur) = start()

	values = [song_ID, user_ID]
	cur.execute('UPDATE users SET last_loved_song=%s WHERE users_ID=%s', 
				values)
	conn.commit()
	end(conn, cur)

def get_user():
	(conn, cur) = start()
	cur.execute('SELECT * from users WHERE times=0')
	result = cur.fetchall() 
	cur.execute('UPDATE users SET times=times-1 WHERE times>0')
	conn.commit()
	end(conn, cur)
	return result

def get_all_users():
	(conn, cur) = start()
	cur.execute('SELECT * from users')
	result = cur.fetchall() 
	end(conn, cur)
	return result


def modify_user(user_ID, record_time):
	(conn, cur) = start()
	cur.execute('UPDATE users SET record_time=%s WHERE users_ID=%s', (record_time, user_ID))
	conn.commit()
	end(conn, cur)



def not_listening(user_ID):
	(conn, cur) = start()
	times = [3, user_ID]
	cur.execute('UPDATE users SET times=%s where users_ID=%s', times)
	conn.commit()
	end(conn, cur)

def logging(time, message):
	(conn, cur) = start()
	values = [str(time), str(message)]
	cur.execute('insert into logging values(%s, %s)', values)
	conn.commit()
	end(conn, cur)







