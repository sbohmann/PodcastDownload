# PodcastDownload

Attention! This script may overrwrite existing files in the current directory! Only call from dedicated directories, usually one per rss feed!

And please don't even think about distributing the files and information acquired by downloading feeds and linked files, using this tool or any other, unless explicitly permitted by the originator and with your full understanding of the terms and limits of such permission.

Syntax:

    python3 <path to script>/podcast_download.py <feed url>

It writes to the current directory. Thus you should not call it from the path containing the script.

You probably need to install the libraries it depends upon, using e.g. pip. Please consult your operating system and python installation specific documentation concerning python modules (and probably mentioning pip) in case you don't quite know what I'm talking about right now.

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
