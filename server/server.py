from flask import Flask
import podcast_list

app = Flask('Podcasts')


@app.route('/')
def index():
    return podcast_list.render()


app.run(debug=True, host='0.0.0.0', port='9100')
