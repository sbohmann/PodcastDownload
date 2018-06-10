
from http.client import HTTPConnection
import feedparser
import wget
import os.path
import sys

GET = "GET"
UTF8 = "utf-8"
DEBUG = False

print(sys.argv)

class PodcastDownload:
    def __init__(self, feed_url):
        self.feed_url = feed_url

    def run(self):
        self.get_raw_feed()
        self.read_feed()
        self.feed = feedparser.parse(self.text)
        if DEBUG: self.pretty_print(self.feed, "")
        self.download_files()

    def get_raw_feed(self):
        connection = HTTPConnection("static.orf.at")
        connection.request(GET, self.feed_url)
        self.feed_response = connection.getresponse()
        if self.feed_response.status != 200:
            raise IOError("Status " + str(self.feed_response.status) + " from http connection")

    def read_feed(self):
        self.text = ""
        while True:
            line = self.feed_response.readline().decode(UTF8)
            if not line: break
            self.text += line
        self.feed_response.close()

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
                filename = wget.detect_filename(url)
                if not os.path.isfile(filename):
                    print("Downloading missing file [" + filename + "]")
                    wget.download(url)
                elif DEBUG:
                    print("Skipping existing file [" + filename + "]")


for argument in sys.argv[1:]:
    if argument.startswith("http://"):
        print("feed url " + argument)
        PodcastDownload(argument).run()
