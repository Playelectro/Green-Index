import os, json, glob

import folium
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)
map = 0


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/map')
def iframe():    
    map.get_root().render()
    header = map.get_root().header.render()
    body_html = map.get_root().html.render()
    script = map.get_root().script.render()
    
    return render_template('map.html', header = header, body_html = body_html, script = script)


def load_marker(data, map, icon):
    return folium.Marker(
        location = data['location'],
        tooltip = data['name'],
        icon = icon
    )
    

if __name__ == '__main__':

    map = folium.Map(
        width = "75%",
        height = "600px",
        location = [45.649208, 24.896366],
        zoom_start = 7,
        min_zoom = 7,
        max_bounds = True,    
        tiles=folium.TileLayer(no_wrap=True)
    )
    
    animal_icon = folium.CustomIcon(
        'static/images/pawprint.png',
        icon_size=(45 , 48)
    )
    
    plant_icon = folium.CustomIcon(
        'static/images/frunza.png',
        icon_size=(45 , 48)
    )
    
    data_path = 'data/'
    
    for j_file in glob.glob(data_path + "protected_species/*.json"):
        if j_file.rfind('template') == -1:
            f = open(j_file, encoding = "utf8")
            js = json.load(f)
            if js['type'] == 'Animal':
                load_marker(js, map, animal_icon).add_to(map)
            else:
                load_marker(js, map, plant_icon).add_to(map)
            print(j_file)
            f.close()

    

    app.run(debug=True)
