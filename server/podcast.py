import os
import re

from flask import render_template


class Podcast:
    def __init__(self, name):
        self.name = name

    def render(self):
        episodes = self._read_episodes()
        return render_template('podcast.html', name=self.name, episodes=episodes)

    def _read_episodes(self):
        latest_episodes_file = self._get_latest_episodes_file()
        if latest_episodes_file:
            return _read_episode_file(latest_episodes_file)
        else:
            return []

    def _get_latest_episodes_file(self):
        episode_dates = list(filter(None, map(_episodes_file_date, os.listdir(self.name))))
        episode_dates.sort()
        return episode_dates[-1] if episode_dates else None


_episodes_file_regex = re.compile('episodes_(\\d{8}T\\d{6}\\.{\\d{6}Z).txt')


def _episodes_file_date(file):
    match = _episodes_file_regex.match(file)
    if match:
        return match[1]
    else:
        return None


def _read_episode_file(file):
    return list(open(file, 'r'))
