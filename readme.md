Worlds greatest python script which creates a list of pivotal stories written by me.

Gives the results that you'd get in doing a filer of created_since in a nice list format.

Requires pytracker, found here: http://code.google.com/p/pytracker/ , which requires other stuff. 

Also makes use of ConfigParser to keep your API key out of the py file, if you want to use that make a separate file called 'config.cfg', and add two lines:

[api_settings]  
pivotal_api_key: YOUR_PIVOTAL_API_KEY_HERE

That's it!

Probably overkill, but I'll bet you can add a bunch of cool stuff to it.