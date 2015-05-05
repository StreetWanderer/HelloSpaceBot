import time
import core


frequencyInSec = 60.0 * 1.0 #every minute
startTime = time.time()
step = frequencyInSec - ((time.time() - startTime) % frequencyInSec)

while True:
	if step > 1:
  		#print "tick - " + time.strftime("%H:%M:%S")
  		core.main(False)
  		step = frequencyInSec - ((time.time() - startTime) % frequencyInSec)
  		time.sleep(step)
  	else:
  		print "Error in step calculation - step="+step