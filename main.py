import json, random, requests, time, re, pytumblr


OPUS_API_BASE_URL = 'http://pds-rings-tools.seti.org/opus/api/'
PLANET_ID_TABLE = {'MER': 'Mercury', 'VEN': 'Venus', 'EAR': 'Earth', 'MAR': 'Mars', 'JUP': 'Jupiter', 'SAT': 'Saturn', 'URA': 'Uranus', 'PLU':'Pluto'}
CRAFT_LIST = [{'craft': 'Cassini', 'pages':1}, 
			  {'craft':'Hubble', 'pages':1}, 
			  {'craft':'Galileo', 'pages':1}, 
			  {'craft':'Voyager', 'pages':1},
			  {'craft':'New Horizons', 'pages':1}
			 ]


def getImagesList(mission, page):
	#Grab the list of images from OPUS and return it as a dictionnary
	
	payload = {'missionid': mission.replace("+", " "), 'page': page}
	imagesList = requests.get(OPUS_API_BASE_URL + 'images/full.json', params=payload)
	parsedImages = json.loads(imagesList.text)
	
	return parsedImages;



def selectRandImage(images):
	#Select a random image in the retrieved list
	#Return full path and missionID
	#Should check against a list of already posted images at some point
	selected = random.choice(images['data'])
	image = {'url': images['path'] + selected['full'], 'ring_obs_id': selected['ring_obs_id']}
	
	return image



def getMissionData(ring_obs_id):
	#Retrieve mission data from OPUS
	missionRawData = requests.get(OPUS_API_BASE_URL + 'metadata/'+ring_obs_id+'.json')
	missionData = json.loads(missionRawData.text)

	return missionData['General Constraints']



def writePostText(missionData, spacecraft):
	#Use mission data to generate the text posted with the picture 
	#Mission Name, Target Photographed, Date, Instrument, OPUS link

	source = 'http://pds-rings-tools.seti.org/opus#/ringobsid='+missionData['ring_obs_id']+'&detail='+missionData['ring_obs_id']+'&view=detail'
	print missionData['ring_obs_id']
	if missionData['target_name'] is None:
		return None

	post = 'A photo of <b>'+missionData['target_name'].title()+'</b>'
	if missionData['target_class'] != 'PLANET':
		if missionData['target_class'][0] in 'aeiou':
			post += ', an '
		else:
			post += ', a '
		post += missionData['target_class'].lower()

		if missionData['target_class'] == 'MOON':
			post += ' of <b>'+PLANET_ID_TABLE[missionData['planet_id']]+'</b>'
		else:
			post += ' near <b>'+PLANET_ID_TABLE[missionData['planet_id']]+'</b>'


	post += '.'
	tweet = striphtml(post)
	post+= '<br />\n'
	post += 'Took by <b>'+spacecraft+'</b> with '+missionData['instrument_id']

	if missionData['time1'] is not None and missionData['time1'] != '00:00:00':
		#print("time is not None, time is "+missionData['time1'])
		date = time.strptime(missionData['time1'].replace("-", ""), "%Y%m%dT%H:%M:%S")
		post += ' on ' + time.strftime("%B %d, %Y at %H:%M:%S", date)

	post += '.<br />\n'
	post += '<br />\n'

	post += '<a href="'+source+'" target="_blank">'
	post += 'Detail page on OPUS database.</a>'


	return {'post':post, 'tweet':tweet, 'source':source }

def postToTumblr(imageURL, text, spacecraft):
	#create the post on Tumblr.
	tumblrClient = pytumblr.TumblrRestClient(
				    '<consumer_key>',
				    '<consumer_secret>',
				    '<oauth_token>',
				    '<oauth_secret>',
					)

	tumblrClient.create_photo('hellospacebot',
							   state="published", 
							   tags=["space", "spaceholiday", spacecraft], 
							   source=imageURL, 
							   caption=text['post'], 
							   tweet=text['tweet']+' [URL]', 
							   link=text['source']
							  )

	print "Published to Tumblr"


	

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)



#master process should randomize a mission choice and page choice.
#should check against "pages done" list at some point

choosenCraft = random.choice(CRAFT_LIST)

photos = getImagesList(choosenCraft['craft'], random.randint(1, choosenCraft['pages']))
imgObj = selectRandImage(photos)
missionDataObj = getMissionData(imgObj['ring_obs_id'])
text = writePostText(missionDataObj, choosenCraft['craft'])
#print imgObj
#print missionDataObj
print imgObj['url']
print  text

if text is not None:
	postToTumblr(imgObj['url'], text, choosenCraft['craft'])


