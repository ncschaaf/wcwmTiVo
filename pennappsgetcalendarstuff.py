#import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

#FLAGS = gflags.FLAGS


print "creating flow"

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret can be found in Google Developers Console
FLOW = OAuth2WebServerFlow(
    client_id= '368112320923-94adjqlcu8e6us5o4bikd6tf0pimrvq0.apps.googleusercontent.com',
    client_secret='ofcK0vZF8hBvDN_K90euBmXy ',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='Test')



print "flow created"



# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)


print "CREATING HTTP CREDENTIALS"


# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)
print "creating SERVICE"
# Build a service object for interacting with the API. Visit
# the Google Developers Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http,
       developerKey='AIzaSyBWoWoYLrkaGHz2sVvtTCZw9Su1L4-zbjs')



print "SERVICE SUCCESSFULLY CREATED"

page_token = None
while True:
  events = service.events().list(calendarId='primary', pageToken=page_token).execute()
  for event in events['items']:
    print event['summary']
  page_token = events.get('nextPageToken')
  if not page_token:
    break


