# Gives the same feedback as filtering "created since," but returns results in a nice list form for using in weekly reports and such
#
# requires pytracker - http://code.google.com/p/pytracker/ , which requires other stuff. 

from pivotal import pivotal
import re
import datetime
import ConfigParser

# Authenticating with your Pivotal API token object, if you'd like to hardcode it, uncomment the line below:
# pv = pivotal.Pivotal('[YOUR_PIVOTAL_API_KEY_HERE]') 

# else, have a companion file called 'config.cfg' that looks like this:
#
# [api_settings]
# pivotal_api_key: YOUR_PIVOTAL_API_KEY_HERE
#
# Easy!

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

pv = pivotal.Pivotal(config.get('api_settings', 'pivotal_api_key'))

# Getting 7 days ago, formatting date to pivotal as mm/dd/yyyy 
today = datetime.date.today()
seven_days_ago = "%s/%s/%s" % (today.month, today.day-7, today.year)

# From the project number specified, get an XML element tree of stories using the date_entry filter
stories_created_since = pv.projects("367235").stories(filter='created_since:%s' % seven_days_ago).get_etree() 

# Container for an array of incrementing numbers to be used as ID's
zip_counter = [] 
counter = 0

# Create an array of numbers matching the number of stories, append the incremented counter to zip_counter array
for items in stories_created_since:
  counter += 1
  zip_counter.append(counter)

# List comprehensions (YES!!!) to iterate through all the XML stories, pulling out specific elements into their own list
story_names = [i[7].text for i in stories_created_since]
requested_by = [i[8].text for i in stories_created_since]
owned_by = [i[9].text for i in stories_created_since]
link = [i[3].text for i in stories_created_since]

# Put all the story item lists back together per story
story_report = list(zip(zip_counter, story_names, requested_by, owned_by, link))

# Displaying Results
print "Displaying all stories added since %s" % seven_days_ago 
print " "

# Iterate through zipped story_report, pulling out elements in order. Ironic that we're now detaching the recently reattached detached elements, no?
for item in story_report:
  # Sometimes if a story doesn't have an owner, it will set the date instead. This RegEx catches any owner that starts with a number
  if re.match("[1-9]+", item[3]):
    owner = "No one"
  else:
    owner = item[3]
  print "%s - Story Name: %s, Requested By: %s, Owned By: %s, Url: %s" % (item[0], item[1], item[2], owner, item[4])
