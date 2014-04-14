#! /usr/bin/env python
# -- encoding:utf - 8 --
import sys
import requests
import re
import time
import pickle
from bs4 import BeautifulSoup
import pylast
import gevent
import logging
import os
from datetime import datetime,timedelta


import database
from album import Track
reload(sys)
sys.setdefaultencoding('utf-8')
API_KEY = "2e6e98ec329aa9c86bb8a541fc09bd29" # this is a sample key
API_SECRET = "c86c14938f3344707b0a56a0a1370e69"


def xiami(user):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0',
			   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			   'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
			   'Accept-Encoding': 'gzip, deflate',
				'DNT': '1',
				'Connection': 'keep-alive'}
	proxies = {'http': 'http://122.226.122.201:8080'}
	xiami_url = 'http://www.xiami.com/space/charts-recent/u/%s'%(user[0])
	r = requests.get(xiami_url, headers=headers)
	soup = BeautifulSoup(r.content)
	last_time = datetime.strptime(user[2], '%Y-%m-%d %H:%M:%S')
	minutes = (datetime.now() - last_time).seconds/60
	track_times = soup.findAll('td', class_='track_time')
	track_times = [re.search(u'\d+', track_time.text).group()
				   for track_time in track_times 
				   if re.search(u'分钟前', track_time.text)]
	second_html = soup.find('td', class_='track_time')
	if second_html:
		second_exist = re.search(u'秒前|刚刚', second_html.text)
	else:
		second_exist = False
	if track_times or second_exist:
		exists_times = [int(track_time) for track_time in track_times
					   if int(track_time)<10]
		track_times = [int(track_time) for track_time in track_times
					   if int(track_time)<minutes]
		#!页面中存在刚刚收听的音乐时间小于十分钟则将times继续设为0
		record_time = None
		if track_times:
			record_time = datetime.now() - timedelta(minutes=track_times[0])
			record_time = record_time.strftime('%Y-%m-%d %H:%M:%S')

		track_times = [int(time.time()-track_time*60) for track_time in track_times]
		if second_exist:
			record_time = datetime.now()
			record_time = record_time.strftime('%Y-%m-%d %H:%M:%S')
			track_times.insert(0, int(time.time()))

		track_number = len(track_times)
		if record_time:
			track_htmls = soup.findAll('tr', id=re.compile('track_\d+'), limit=track_number)
			upper_htmls = [track_html.find('td', class_='song_name') for track_html in track_htmls]
			artists_html = [artist_html.findAll('a')[1:] for artist_html in upper_htmls]
			artists = []
			for artist in artists_html:
				all_artists = [one_artist.text for one_artist in artist
								if not re.search('http://i.xiami.com',
												 one_artist['href'])]
				all_artist = '&'.join(all_artists)
				artists.append(all_artist)
			title_htmls = soup.findAll('a', href=re.compile('/song/\d+'), limit=track_number)
			titles = [title['title'] for title in title_htmls]
			return (titles, artists, track_times, record_time)
		elif exists_times:
			database.modify_user(user[0], user[2])
			return (None, None, None, None)
		else:
			database.not_listening(user[0])
			return (None, None, None, None)
	else:
		database.not_listening(user[0])
		return (None, None, None, None)

def xiami_loved(user):
	user_ID = user[0]
	last_loved_song = database.get_last_loved_song(user[0])
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0',
			   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			   'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
			   'Accept-Encoding': 'gzip, deflate',
				'DNT': '1',
				'Connection': 'keep-alive'}

	r = requests.get('http://www.xiami.com/space/feed/u/%s/type/9'%(
					  user_ID), headers = headers)
	soup = BeautifulSoup(r.content)
	songs_IDs_htmls = soup.findAll('a', {'target':'_blank'},
									href=re.compile('/song/\d+'))
	songs_IDs = [re.search('/song/(\d+)', songs_IDs_html['href']).group(1)
				 for songs_IDs_html in songs_IDs_htmls]
	if last_loved_song == 'None':
		loved_songs_IDs = songs_IDs
	elif last_loved_song in songs_IDs:
		place = songs_IDs.index(last_loved_song)
		loved_songs_IDs = songs_IDs[0 : place]
	else:
		loved_songs_IDs = songs_IDs

	loved_songs = []
	for loved_song_ID in loved_songs_IDs:
		r = requests.get('http://www.xiami.com/song/%s'%(loved_song_ID),
							headers=headers)
		soup = BeautifulSoup(r.content)
		title_html = soup.title.text
		title = title_html[:-2]
		album_artist_html = soup.find('table', id='albums_info')
		#There are some rare and special cases where the url doesn't fit 
		#the normal one,so just ignore it.
		if not album_artist_html:
			continue
		album_html = album_artist_html.find('a', 
											href=re.compile('/album/\d+'))
		album = album_html['title']
		artists_htmls = album_artist_html.findAll('tr')[1]
		artists_htmls = artists_htmls.findAll('a')
		artists = [artist_html.text for artist_html in artists_htmls]
		artist = '&'.join(artists)
		track = Track(loved_song_ID, title, album, artist)
		loved_songs.append(track)
	return loved_songs		
def lastfm_loved(loved_songs, user):
	'''
	Scrobble the user's today loved songs to the Last fm 
	# Parameters:
	* loved_songs: one user's loved songs
	* user: specific user
	'''
	network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
	    API_SECRET)
	network.session_key = user[1]
	for loved_song in loved_songs:
		track = pylast.Track(loved_song.artist, loved_song.title, network)
		track.love()
	database.modify_last_loved_song(user[0], loved_songs[0].song_ID)


def get_session(token):
	network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
	    API_SECRET)
	sg = pylast.SessionKeyGenerator(network)
	session_key = sg.get_web_auth_session_key(token)
	return session_key	

def lastfm(titles, artists, track_times, user):
	network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
	    API_SECRET)
	session_key = user[1]
	network.session_key = session_key
	#if the music is playing on
	if (time.time()-track_times[0])<180:
		network.update_now_playing(artists[0], titles[0])

	def scrobble(title, artist, timestamp):
		network.scrobble(artist, title, timestamp)

	def get_spawns():
		spawns = [gevent.spawn(scrobble, title, artist, timestamp)
				  for title, artist, timestamp 
				  in zip(titles, artists, track_times)]
		return spawns
	gevent.joinall(get_spawns())

if __name__ == '__main__':
	xiami_loved((168488, '33'))


