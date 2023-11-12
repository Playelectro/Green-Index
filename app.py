import os
import folium as fol
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/map')
def iframe():
    m = fol.Map(
        width = "75%",
        height = "600px",
        location = [45.649208, 24.896366],
        zoom_start = 7,
        min_zoom = 7,
        max_bounds = True,
    )
    
    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()
    
    return render_template('map.html', header = header, body_html = body_html, script = script)

if __name__ == '__main__':
   app.run(debug=True)
