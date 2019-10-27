from flask import Flask
import os

import podcast_list

app = Flask('Podcasts')
server_directory = os.path.dirname(os.path.abspath(__file__))
template_directory = os.path.join(server_directory, 'templates')


@app.route('/')
def index():
    return podcast_list.render()


app.run(debug=True, host='0.0.0.0', port='9100', template_folder=template_directory)
