# PodcastDownload

Attention! This script may overrwrite existing files in the current directory! Only call from dedicated directories, usually one per rss feed!

Syntax:

    python3 <path to script>/podcast_download.py <feed url>

It writes to the current directory. Thus you will should not call it from the path containing the script.

When downloading a feed for file files with status code 403 firbidden, I set usually succeed by setting a the user agent to the magic value 'Marquise'.

Some web servers expect at least something as the user agent, I think I've seen this with most often with the IIS.

Just add this argument to your call (without the ...)

    ... --user-agent:Marquise

There's nothing special about this user agent name, as far as I know; it's simply a non-empty string ^^

In case an SSL / TLS certificate is broken, there is the very dangerous option

    --dangerously-ignore-ssl-validity

It is really dangerous because you're back to the security level of http (without the s) and downloaded files might thus contain anything!!!

There's also the option

    --debug

in case you're curious what's going on ^^
