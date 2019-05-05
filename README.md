# PodcastDownload

When downloading a feed for file files with status code 403 firbidden, I set usually succeed by setting a the user agent to the magic value 'Marquise'.

Some web servers expect at least something as the user agent, I think I've seen this with most often with the IIS.

Just add this argument to your call (without the ...)

... --user-agent:Marquise

There's nothing special about this user agent name, as far as I know; it's simply a non-empty string ^^
