import datetime
import os.path
import ssl
import sys
import traceback
import urllib.request

import feedparser
import wget

GET = "GET"
UTF8 = "utf-8"
DEBUG = False
DANGEROUSLY_IGNORE_SSL_VALIDITY = False

print(sys.argv)


class PodcastDownload:
    def __init__(self, feed_url):
        self.feed_url = feed_url
        self.feed = None
        self.text = None

    def run(self):
        self.read_feed()
        self.feed = feedparser.parse(self.text)
        if DEBUG: self.pretty_print(self.feed, "")
        self.download_files()

    def read_feed(self):
        feed_filename = self.create_feed_filename()
        wget.download(self.feed_url, feed_filename)
        feed_response = urllib.request.urlopen(self.feed_url)
        self.read_response_text(feed_response)
        feed_response.close()

    def create_feed_filename(self):
        utc_timestamp = datetime.datetime.utcnow()
        utc_timestamp_string = "%04d%02d%02dT%02d%02d%02d.%02dZ" %\
                             (utc_timestamp.year,
                              utc_timestamp.month,
                              utc_timestamp.day,
                              utc_timestamp.hour,
                              utc_timestamp.minute,
                              utc_timestamp.second,
                              utc_timestamp.microsecond)
        return "downloads/feed_" + utc_timestamp_string + ".xml"

    def read_response_text(self, feed_response):
        self.text = ""
        while True:
            line = feed_response.readline().decode(UTF8)
            if not line: break
            self.text += line

    def pretty_print(self, value, indentation):
        if isinstance(value, dict):
            for field in value:
                print(indentation, field, sep="")
                self.pretty_print(value[field], indentation + "    ")
        elif isinstance(value, list):
            index = 0
            for element in value:
                print(indentation, "[", index, "]", sep="")
                index += 1
                self.pretty_print(element, indentation + "    ")
        elif value:
            print(indentation + str(value))

    def download_files(self):
        for entry in self.feed.entries:
            for link in entry.links:
                url = link.href
                original_filename = wget.detect_filename(url)
                _, extension = os.path.splitext(original_filename)
                raw_filename = entry.title
                filename = 'downloads/' + clean_filename(raw_filename) + extension
                if not os.path.isfile(filename):
                    print("Downloading missing file [" + filename + "]")
                    wget.download(url, filename)
                elif DEBUG:
                    print("Skipping existing file [" + filename + "]")


def clean_filename(name):
    result = []
    for char in name:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z' or '0' <= char <= '9':
            result.append(char)
        elif ord(char) > 128:
            result.append(char)
        else:
            result.append('_')
    return ''.join(result)


if __name__ == '__main__':
    feed_urls = []

    for argument in sys.argv[1:]:
        if argument.startswith("http://") or argument.startswith("https://"):
            feed_urls.append(argument)
        elif argument == '--dangerously-ignore-ssl-validity':
            DANGEROUSLY_IGNORE_SSL_VALIDITY = True
        else:
            print("ignoring argument [" + argument + "]")

    if DANGEROUSLY_IGNORE_SSL_VALIDITY:
        # This is an unfortunate hack. urllib.urlretrieve does not support a context.
        # Thus, a global override is installed. Please, really never, ever do this
        # in larger projects where it would affect EVERYTHING else.
        # Here, there is nothing else, of course, unless you misappropriate this script
        # as a library.
        # Dont't do that under any circumstances!!!!!!!
        # The above if __name__ is '__main__' safeguard is intended to prevent effects
        # in the case of such use as a library but please, do not rely on this!!!
        # And also, please do not copy the following line into any base of code,
        # it really turns of ANY checks against SSL validity.
        ssl._create_default_https_context = ssl._create_unverified_context

    for url in feed_urls:
        try:
            print("feed url " + url)
            PodcastDownload(url).run()
        except Exception as error:
            traceback.print_exc()
