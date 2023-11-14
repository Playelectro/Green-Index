import os, json, glob

import folium
from flask import (Flask, render_template, request,
                   send_from_directory)


app = Flask(__name__)
map = 0
map_js = 0

marker_list = []
area_list = [[]]

marker_area = 0.5

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/background.jpg')
def background():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'images/image_background.jpg')

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
    
    args = request.args
    
    if args.get('click_lat') is not None:
    
        click_lat = float(args.get('click_lat'))
        click_lon = float(args.get('click_lon'))
    
        #load_marker_info(click_lat, click_lon)        
        

    
    return render_template('map.html', header = header, body_html = body_html, script = script)


def load_marker_info(lat, lon):

    
    for marker in marker_list:
        location = marker['location']
        if abs(location[0] - lat) <= marker_area and abs(location[1]-lon) <= marker_area:
            print(marker['name'])
    

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
        
    
    data_path = 'data/'
    
    for j_file in glob.glob(data_path + "protected_species/*.json"):
        if j_file.rfind('template') == -1:
            f = open(j_file, encoding = "utf8")
            js = json.load(f)
            i = 0
            
            while i < len(js['location']):
                if js['type'] == 'Animal':
                    folium.Marker(location = js['location'][i], tooltip = js['name'],icon = folium.CustomIcon('static/images/pawprint.png',icon_size=(45 , 48))).add_to(map)
                else:
                    folium.Marker(location = js['location'][i], tooltip = js['name'],icon = folium.CustomIcon('static/images/frunza.png',icon_size=(45 , 48))).add_to(map)
                i+=1
                
            
            
            
            marker_list.append(js)
            
            f.close()
    
    app.run(debug=True)
