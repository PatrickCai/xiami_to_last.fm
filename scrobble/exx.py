import pylast
# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account for Last.fm
API_KEY = "2e6e98ec329aa9c86bb8a541fc09bd29" # this is a sample key
API_SECRET = "c86c14938f3344707b0a56a0a1370e69"


network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
    API_SECRET)

# sg = pylast.SessionKeyGenerator(network)
# token = 'f867636109d055599249a97f34084124'
# session_key = sg.get_web_auth_session_key(token)
# session_key = '1a91ae8be6dcc41774b952cb14246275'


# session_key = '21df9442e1b6cdd290d06d901ca9ab61'
session_key = '8a546b73099e717230bdb791623bdfc6'
network.session_key = session_key
print(network.get_authenticated_user())

2326114
48474
# artist = 'Bill Callahan'
# track = "Riding For the Feeling"

# song = pylast.Track(artist, track, network)
# song.love()



# print song.get_album()

# timestamp = '1394722800'

# network.scrobble(artist, track, timestamp, pylast.SCROBBLE_SOURCE_USER, pylast.SCROBBLE_MODE_PLAYED, 0)
# from datetime import datetime,timedelta
# import time
# kkd = []
# print(len(kkd))