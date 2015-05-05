Hello Space Bot
==============
A bot that extracts random photos from the OPUS database and post them to Tumblr with a description of what the picture is about.

&nbsp;  

About the code
---
Grab pictures from the NASA/SETI [OPUS database](http://pds-rings-tools.seti.org/opus) using the JSON API.  
The script then extract the mission data and tries to make sens of it. It then generates an HTML snippet that is posted alongside the picture to Tumblr.  
Most of the complexity comes from handling the messiness of the data without causing the script to exit.

Possible Improvements
---
* Add the picture in the tweet
* Search more time indicators for when the picture was taken 
  * there is sometimes a timestamp in *&lt;probe-name&gt; LORRI  Constraints*
* Avoid posting the same picture twice
  * maybe store posted IDs somewhere
* Add snarky and overly enthusiastic comments to posts
