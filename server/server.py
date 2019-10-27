from flask import Flask
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
def index(name):
    return podcast.Podcast(name).render()


app.run(debug=True, host='0.0.0.0', port='9100')
