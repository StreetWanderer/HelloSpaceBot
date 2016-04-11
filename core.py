import json, random, requests, time, pytumblr
import config, utils




def getImagesList(mission, page):
	#Grab the list of images from OPUS and return it as a dictionnary
	
	payload = {'missionid': mission.replace("+", " "), 'page': page}
	imagesList = requests.get(config.OPUS_API_BASE_URL + 'images/full.json', params=payload)
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
	missionRawData = requests.get(config.OPUS_API_BASE_URL + 'metadata/'+ring_obs_id+'.json')
	missionData = json.loads(missionRawData.text)

	return missionData['General Constraints']



def writePostText(missionData, spacecraft):
	#Use mission data to generate the text posted with the picture 
	#Mission Name, Target Photographed, Date, Instrument, OPUS link

	source = 'http://pds-rings-tools.seti.org/opus#/ringobsid='+missionData['ring_obs_id']+'&detail='+missionData['ring_obs_id']+'&view=detail'
	#print missionData['ring_obs_id']
	if missionData['target_name'] is None:
		return None

	post = 'A photo of <b>'+missionData['target_name'].title()+'</b>'
	if missionData['target_class'] != 'PLANET':
		if missionData['target_class'][0] in 'aeiou':
			post += ', an '
		else:
			post += ', a '
		post += missionData['target_class'].lower()

		if missionData['planet_id'] is not None:
			if missionData['target_class'] == 'MOON':
				post += ' of <b>'+config.PLANET_ID_TABLE[missionData['planet_id']]+'</b>'
			else:
				post += ' near <b>'+config.PLANET_ID_TABLE[missionData['planet_id']]+'</b>'


	post += '.'
	tweet = utils.striphtml(post)
	post+= '<br />\n'
	post += 'Taken by <b>'+spacecraft+'</b> with '+missionData['instrument_id']

	if missionData['time1'] is not None and missionData['time1'] != '00:00:00':
		#print("time is not None, time is "+missionData['time1'])
		missionDate = missionData['time1'].replace("-", "").split(".")[0]
		try:
			date = time.strptime(missionDate, "%Y%m%dT%H:%M:%S")
		except ValueError:
			try:
				date = time.strptime(missionDate, "%Y%jT%H:%M:%S")
			except ValueError:
				print 'Time is invalid: '+missionData['time1']
			else:
				post += ' on ' + time.strftime("%B %d, %Y at %H:%M:%S", date)
		else:
			post += ' on ' + time.strftime("%B %d, %Y at %H:%M:%S", date)

	post += '.<br />\n'
	post += '<br />\n'

	post += '<a href="'+source+'" target="_blank">'
	post += 'Detail page on OPUS database.</a>'


	return {'post':post, 'tweet':tweet, 'source':source }

def postToTumblr(imageURL, text, spacecraft):
	#create the post on Tumblr.
	tumblrClient = pytumblr.TumblrRestClient(
				    config.CONSUMER_KEY,
				    config.CONSUMER_SECRET,
				    config.OAUTH_TOKEN,
				    config.OAUTH_SECRET,
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


def main(post):
	#master process should randomize a mission choice and page choice.
	#should check against "pages done" list at some point

	choosenCraft = utils.weighted_choice(config.CRAFT_LIST)

	photos = getImagesList(choosenCraft['craft'], random.randint(1, choosenCraft['pages']))
	imgObj = selectRandImage(photos)
	text = None

	if 'not_found' not in imgObj['url'] or 'http' not in imgObj['url']:
		missionDataObj = getMissionData(imgObj['ring_obs_id'])
		text = writePostText(missionDataObj, choosenCraft['craft'])
	

	if post is False and text is not None:
		print imgObj['ring_obs_id']+" -> "+imgObj['url']
		print utils.striphtml(text['post'])
	elif text is not None:
		print imgObj['url']
		print utils.striphtml(text['post'])
		postToTumblr(imgObj['url'], text, choosenCraft['craft'])
	else:
		print 'Error while generating post for'+imgObj['ring_obs_id']+'.\nSkipping.'
	
		
	print '\n----------------------\n'
