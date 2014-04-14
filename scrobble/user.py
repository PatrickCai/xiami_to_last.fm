#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import requests
import re
import urllib2
import pylast
import database
import logging
reload(sys)
sys.setdefaultencoding('utf-8')

def verify_user(user_ID):
	should_continue = database.is_user_exist(user_ID)
	return should_continue



API_KEY = "2e6e98ec329aa9c86bb8a541fc09bd29" 
API_SECRET = "c86c14938f3344707b0a56a0a1370e69"
def get_url(user_ID):
	network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
	    API_SECRET)
	sg = pylast.SessionKeyGenerator(network)
	if (re.search('/Users/cai/caiProject/django_project/',sys.path[0])):
		callback_url = 'http://127.0.0.1:8000/third?username=%s'%(user_ID)
	else:
		callback_url= 'http://scrobble.chom.me/third?username=%s'%(user_ID)
	url = sg.get_web_auth_url(callback_url)
	return url,network


if __name__ == '__main__':
	verify_user(168488)