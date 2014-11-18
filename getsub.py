import sys
import os
import hashlib
import urllib
import urllib2

EXTENSOES = ['avi', 'mkv', 'mp4']


def get_hash(name):
	readsize = 64 * 1024
	with open(name, 'rb') as f:
		size = os.path.getsize(name)
		data = f.read(readsize)
		f.seek(-readsize, os.SEEK_END)
		data += f.read(readsize)
	return hashlib.md5(data).hexdigest()
	

def cataLegenda(filme):	
	if filme[-3:] not in EXTENSOES:
		return "extensao desconhecida"
	
	if os.path.isfile(filme[:-4]+".srt"):
		return "arquivo de legenda ja existe"
	
	data = urllib.urlencode({"action": "download", 
							 "hash": get_hash(filme), 
							 "language": "pt" })
	url = "http://api.thesubdb.com/"
	headers = {'User-agent': 'SubDB/1.0 (PlexScript/0.1; http://plex.com/)'}
	req = urllib2.Request(url+"?"+data, None, headers)
	
	try:
		resp = urllib2.urlopen(req)
	except urllib2.HTTPError as e:
		return e.read()
		
	subs = resp.read()
	
	if subs:
		srtname = filme[:-4]+'.srt'
		srt = open(srtname, 'w')
		srt.write(subs)
	else:
		return "legenda nao encontrada"
	
if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.exit("parametros insuficientes")
	
	if os.path.isdir(sys.argv[1]):
		for filme in os.listdir(sys.argv[1]):
			cataLegenda(sys.argv[1]+"/"+filme)
	else:
		sys.exit(cataLegenda(sys.argv[1]))
