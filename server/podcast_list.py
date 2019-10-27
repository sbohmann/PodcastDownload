from flask import render_template
import os


def render():
    print(_podcast_names())
    return render_template('podcast_list.html', names = _podcast_names())


def _podcast_names():
    result = []
    for file in os.listdir('.'):
        if file != 'PodcastDownload' and os.path.isdir(file):
            result.append(file)
    result.sort()
    return result
