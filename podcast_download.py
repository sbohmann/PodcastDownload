import datetime
import os.path
import ssl
import sys
import time
import traceback

import feedparser
import requests
import wget

import filenames
import print_feed

GET = "GET"
UTF8 = "utf-8"
DEBUG = False
DANGEROUSLY_IGNORE_SSL_VALIDITY = False
USER_AGENT = None

print(sys.argv)


class PodcastDownload:
    def __init__(self, feed_url):
        self.utc_timestamp = datetime.datetime.utcnow()
        self.utc_timestamp_string = create_utc_timestamp_string(self.utc_timestamp)
        self.feed_url = feed_url
        self.feed = None
        self.feed_text = None
        self.downloaded_episode_filenames = []
        self.next_feed = None

    def run(self):
        self.read_feed()
        self.feed = feedparser.parse(self.feed_text)
        self.fetch_next_feed()
        if DEBUG:
            print_feed.pretty_print_feed(self.feed)
        self.download_files()
        self.write_episodes_file()

    def fetch_next_feed(self):
        try:
            for link in self.feed.feed.links:
                if link.rel == 'next':
                    self.next_feed = link.href
        except Exception as _:
            traceback.print_exc()

    def read_feed(self):
        self.feed_text = download_file(self.feed_url, self.create_feed_filename(), True)

    def create_feed_filename(self):
        return "feed_" + self.utc_timestamp_string + ".xml"

    def download_files(self):
        for entry in self.feed.entries:
            for link in entry.links:
                self.try_download_file(entry, link)

    def try_download_file(self, entry, link):
        try:
            self.download_file(entry, link)
        except Exception as _:
            traceback.print_exc()

    def download_file(self, entry, link):
        entry_url = link.href
        original_filename = wget.detect_filename(entry_url)
        if original_filename == 'download.wget':
            extension = ''
        else:
            _, extension = os.path.splitext(original_filename)
        raw_filename = entry.title
        filename = filenames.clean_filename(raw_filename) + extension
        self.downloaded_episode_filenames.append(filename)
        if not os.path.isfile(filename):
            print("Downloading missing file [" + filename + "]")
            download_file(entry_url, filename)
        elif DEBUG:
            print("Skipping existing file [" + filename + "]")

    def write_episodes_file(self):
        filename = "episodes_" + self.utc_timestamp_string + ".txt"
        file = open(filename, 'w')
        for episode_filename in self.downloaded_episode_filenames:
            file.write(episode_filename + '\n')
        file.close()


def create_utc_timestamp_string(utc_timestamp):
    return "%04d%02d%02dT%02d%02d%02d.%02dZ" % \
                           (utc_timestamp.year,
                            utc_timestamp.month,
                            utc_timestamp.day,
                            utc_timestamp.hour,
                            utc_timestamp.minute,
                            utc_timestamp.second,
                            utc_timestamp.microsecond)


def download_file(file_url, filename, return_text=False):
    headers = {'User-Agent': USER_AGENT} if USER_AGENT else {}
    result = requests.get(file_url, headers=headers)
    if not result.ok:
        raise ValueError('Request to url [' + file_url + '] failed f=with status code ' + str(result.status_code))
    temporary_filename = filename + '.temp.' + str(time.time())
    file = open(temporary_filename, 'wb')
    file.write(result.content)
    file.close()
    os.rename(temporary_filename, filename)
    if return_text:
        return result.content.decode(UTF8)


if __name__ == '__main__':
    feed_urls = []

    for argument in sys.argv[1:]:
        user_agent_prefix = '--user-agent:'
        if argument.startswith("http://") or argument.startswith("https://"):
            feed_urls.append(argument)
        elif argument == '--debug':
            DEBUG = True
        elif argument == '--dangerously-ignore-ssl-validity':
            DANGEROUSLY_IGNORE_SSL_VALIDITY = True
        elif argument.startswith(user_agent_prefix):
            USER_AGENT = argument[len(user_agent_prefix):]
        else:
            print("ignoring argument [" + argument + "]")

    if len(feed_urls) > 1:
        raise ValueError('attempting to download multiple feeds at once: ' + str(feed_urls))

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
        # it really turns off ANY checks against SSL validity.
        ssl._create_default_https_context = ssl._create_unverified_context

    for url in feed_urls:
        try:
            next_feed = url
            while next_feed:
                print("feed url " + next_feed)
                download = PodcastDownload(next_feed)
                download.run()
                next_feed = download.next_feed
        except Exception as _:
            traceback.print_exc()
