from flask import Flask, send_from_directory
import os

import podcast_list
import podcast

server_directory = os.path.dirname(os.path.abspath(__file__))
template_directory = os.path.join(server_directory, 'templates')
app = Flask('Podcasts', template_folder=template_directory)


@app.route('/')
def index():
    return podcast_list.render()


@app.route('/podcast/<name>')
def podcast_page(name):
    return podcast.Podcast(name).render()


@app.route('/podcast/<name>/episode/<episode>')
def podcast_episode(name, episode):
    return send_from_directory(directory=name, filename=episode)


app.run(host='0.0.0.0', port='9100')
