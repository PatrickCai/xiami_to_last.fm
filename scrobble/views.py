import re
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import os
import requests
import user
import scrobble
import database
import logging
from datetime import datetime, timedelta
# Create your views here.
# os.environ['disable_fetchurl'] = "1"
def hello(request):
	r = requests.get('http://www')
	dd = r.content
	return	HttpResponse(dd)

def verify(request):
	user_ID = request.GET.get('username')
	should_continued = user.verify_user(user_ID)
	return HttpResponse(should_continued)
		
def love(request):
	number_of_task = int(request.GET.get('cron'))
	all_users = database.get_all_users()
	all_users = sorted(all_users, key=lambda x:x[0])
	slice_number = len(all_users) / 5
	if number_of_task != 4:
		users = all_users[number_of_task*slice_number:
						  (number_of_task+1)*slice_number]
	elif number_of_task == 4:
		users = all_users[number_of_task * slice_number:
						  len(all_users)]
	for user in users:
		loved_songs = scrobble.xiami_loved(user)
		if loved_songs:
			scrobble.lastfm_loved(loved_songs, user)

	return HttpResponse('Loved!')

def auth(request):
	user_ID = request.GET.get('username')
	(url, network) = user.get_url(user_ID)
	return render(request, 'second.html', {"url": url},)


def record(request):
	token = request.GET.get('token')
	session = scrobble.get_session(token)
	user_ID = request.GET.get('username')
	record_time = datetime.now() - timedelta(minutes=20)
	record_time = record_time.strftime('%Y-%m-%d %H:%M:%S')
	database.insert_user(user_ID, session, record_time)
	return render(request, 'third.html')


def run(request):
	#read the user list from database
	users = database.get_user()
	for user in  users:
		#read playing songs from the xiami
		titles, artists, track_times, record_time = scrobble.xiami(user)
		if titles:
			scrobble.lastfm(titles, artists, track_times, user)

			#modify the user information
			database.modify_user(user[0], record_time)
	return HttpResponse('running!')