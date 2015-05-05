import time
import core


#frequencyInSec = 60.0 * 1.0 #every minute
frequencyInSec = 60.0 * 30.0 #every 30 minutes
postToTumblr = True



startTime = time.time()
step = frequencyInSec - ((time.time() - startTime) % frequencyInSec)

while True:
	if step > 1:
  		#print "tick - " + time.strftime("%H:%M:%S")
  		core.main(postToTumblr)
  		step = frequencyInSec - ((time.time() - startTime) % frequencyInSec)
  		time.sleep(step)
  	else:
  		print "Error in step calculation - step="+step