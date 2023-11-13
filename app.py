import os, json, glob

import folium
from flask import (Flask, render_template, request,
                   send_from_directory)

app = Flask(__name__)
map = 0
map_js = 0


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
    
    map_js = find_var_name(script, "var map_")
    
    pstart, pend = find_popup_slice(script)
    
    # Inject code to get map clicks :)
    script = script[:pstart] + inject_popup_code() + script[pend:]    
    
    text = request.args.get('click_lat')
    if text is not None:
        print()
        print('click_lat:' + text)
        print()

    return render_template('map.html', header = header, body_html = body_html, script = script)


def load_marker(data, map, icon):
    return folium.Marker(
        location = data['location'],
        tooltip = data['name'],
        icon = icon
    )

def find_var_name(html,pattern):
    
    starting_index = html.find(pattern) + 4
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index
    
    return html[starting_index:ending_index]


def find_popup_slice(html):
    
    pattern =  "function latLngPop(e)"
    
    starting_index = html.find(pattern)
    
    tmp_html = html[starting_index:]

    
    found = 0
    index = 0
    opening_found = False
    while not opening_found or found > 0:
        if tmp_html[index] == '{':
            found += 1
            opening_found = True
        elif tmp_html[index] == '}':
            found -= 1
        index +=1
    
    ending_index = starting_index + index
    
    return starting_index, ending_index
            
def inject_popup_code():
    return '''
    function latLngPop(e) {
              $.ajax({
                  url: '',
                  type: 'get',
                  contentType: 'application/json',
                  data: {
                      click_lat: e.latlng.lat,
                      click_lon: e.latlng.lng
                  },
                  success: function(response){}
              })
        }
    '''

if __name__ == '__main__':

    map = folium.Map(
        width = "75%",
        height = "600px",
        location = [45.649208, 24.896366],
        zoom_start = 7,
        max_bounds = True,    
        tiles=folium.TileLayer(no_wrap=True)
    )
    
    folium.LatLngPopup().add_to(map)
        
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
