# parser.py

BASE_URL = 'https://www.google.com/calendar/feeds/wcwm.wm@gmail.com/public/basic'
INCLUDE_FUTURE = 'futureevents=true'
START_TIME_ORDER = 'orderby=starttime'
ASCENDING = 'sortorder=ascending'
EXPAND_RECURRING = 'singleevents=true'
MAX_RESULTS = 'max-results=10'
CAL_URL = BASE_URL + '?' + \
          INCLUDE_FUTURE + '&' + \
          START_TIME_ORDER + '&' + \
          ASCENDING + '&' + \
          EXPAND_RECURRING + '&' + \
          MAX_RESULTS

import feedparser
cal = feedparser.parse(CAL_URL)
for entry in cal.entries:
    title = entry['title']
    updated = entry['updated']
    summary = entry['summary']
    when = summary.split('&')[0]
    print title.encode('utf8', 'strict'), when.encode('utf8', 'strict')
