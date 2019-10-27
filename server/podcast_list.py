from flask import render_template
import os


def render():
    print(_podcast_names())
    return render_template('podcast_list.html', names = _podcast_names())


def _podcast_names():
    result = []
    for file in os.listdir('.'):
        if _relevant_filename(file):
            result.append(file)
    result.sort()
    return result


def _relevant_filename(file):
    return os.path.isdir(file) and not _excluded_filename(file)


def _excluded_filename(file):
    return file != 'PodcastDownload' and not file.startswith('.')
