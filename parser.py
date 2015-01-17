# parser.py

import re
import feedparser
import string

BASE_URL = 'https://www.google.com/calendar/feeds/wcwm.wm@gmail.com/public/basic'
INCLUDE_FUTURE = 'futureevents=true'
START_TIME_ORDER = 'orderby=starttime'
ASCENDING = 'sortorder=ascending'
EXPAND_RECURRING = 'singleevents=true'
MAX_RESULTS = 'max-results=20'
CAL_URL = BASE_URL + '?' + \
          INCLUDE_FUTURE + '&' + \
          START_TIME_ORDER + '&' + \
          ASCENDING + '&' + \
          EXPAND_RECURRING + '&' + \
          MAX_RESULTS





####
wantstrings = ['test', 'foobar', 'many', 'long']
####



print CAL_URL
cal = feedparser.parse(CAL_URL)
for entry in cal.entries:
    title = entry['title']
    updated = entry['updated']
    summary = entry['summary']
    when = summary.split('&')[0]
    #print title.encode('utf8', 'strict'), when.encode('utf8', 'strict')
    #print summary
    if True: #can filter by search terms here, but not necessary   #any(term.lower() in title.lower() or term.lower() in summary.lower() for term in wantstrings):
        print "\n\n"
        print when
        outfileprelim =  str(title + "_"+when.split()[2]+when.split()[3][:-1])
        outfile = outfileprelim.translate(string.maketrans("",""), string.punctuation) + ".mp3"
        print outfile
        month = when.split()[2]
        day = when.split()[3]
        pattern  = re.compile("(?P<start>(?P<shour>\d\d?)(?P<smin>\:\d\d?)?(?P<sap>am|pm)) to (?P<ehour>\d\d?)(?P<emin>\:\d\d?)?(?P<eap>am|pm)")
        mat = pattern.search(when)
        sap = mat.group('sap')
        eap = mat.group('eap')
        ehour = int(mat.group('ehour'))
        shour = int(mat.group('shour'))
        smin = int(mat.group('smin')[1:]) if mat.group('smin') else 0
        emin = int(mat.group('emin')[1:]) if mat.group('emin') else 0
        hours = 0
        minutes = 0
        if sap == "pm":
            shour += 12
        if eap == "pm":
            ehour += 12
        if eap == "am" and ehour == 12:
            ehour = 0
        if sap == "am" and shour == 12:
            shour = 0
        if ehour >= shour:
            hours = ehour - shour
            minutes = emin - smin
            print hours
            print minutes
        else:
            if eap != "am" or sap!= "pm":
                print "ERROR: unexpected times, may be out of order"
            else:
                bmidhour = 24 - shour
                hours = bmidhour + ehour
                bmidmin= 0 - smin
                minutes = bmidmin + emin
                print hours
                print minutes
        length = hours * 60 * 60 + minutes*60
        recordcommand = "cvlc http://wcwm.listen-it.com:8000/ --sout \""+outfile+"\" --run-time="+str(length)+" vlc://quit"
        print recordcommand
        fullbashcommand = "echo '"+recordcommand+"' | at "+mat.group('start')
        

        print fullbashcommand





