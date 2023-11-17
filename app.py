import os, json, glob

import folium

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as Poly

from folium.map import (Marker, LayerControl)
from folium.plugins import (MarkerCluster, Search)
from folium import Polygon
from flask import (Flask, render_template, redirect, request,
                   send_from_directory, )

from jinja2 import Template

app = Flask(__name__)

marker_list = []
area_list = []

rules = []


@app.route('/')
def index():
   return iframe()

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/solutions')
def solutions():
    return render_template('solutions.html')

@app.route('/species')
def species_page():
    return species_entry()

@app.route('/nature_reserve')
def nature_reserves_page():
    return render_template('nature_reserve.html', list= area_list)
    

def iframe():
    map.get_root().render()
    header = map.get_root().header.render()
    body_html = map.get_root().html.render()
    
    click_js = """function onClick(e) {
                    $.ajax({
                        url: '',
                        type: 'get',
                        contentType: 'application/json',
                        data: {
                            click_lat: e.latlng.lat,
                            click_lon: e.latlng.lng
                        },
                        success: function(response){
                            update_page(response);
                            showSlides(0);
                        }
                    })
                }
                """
                 
    e = folium.Element(click_js)
    
    map.get_root().script._children[e.get_name()] = e
    
    script = map.get_root().script.render()
    
    args = request.args
    
    intrest_data = ""
    div_marker = "no_class"
    
    if args.get('click_lat') is not None:
    
        click_lat = float(args.get('click_lat'))
        click_lon = float(args.get('click_lon'))

        
        intrest_data =load_marker_info(click_lat, click_lon)
        
        if intrest_data is None:
            intrest_data = load_reser_info(click_lat,click_lon)
            
        if intrest_data is not None:
            div_marker = "item_first"
        
        return format_data(intrest_data)
                        
    return render_template('index.html', header = header, body_html = body_html, script = script, interest_data = intrest_data)


def load_marker_info(lat, lon):
    for marker in marker_list:
        location = marker['location']
        for i in range(0, len(location)):
            if location[i][0] == lat and location[i][1] == lon:
                return marker
    return None

def load_reser_info(lat, lon):
    for res in area_list:
        poly = Poly(res['area'])
        if poly.contains(Point(lat,lon)):
            return res
    return None



def format_data(data):
    
    title = f"<h1>{data['name']}</h1>"
  #  if data.get('status') is None or len(data['status']) == 0  or data['status'].find("default") != -1:
  #      title = f"<h1>{data['name']}</h1>"
  #   else:
  #      title = f"<h1>{data['name']} - {data['status']}</h1>"
  
    suggestions = ""        
    
    if data.get('type') is not None:
        if data['type'] == "Fish":
            suggestions = rules['fish']
        elif data['type'] == "Plants":
            suggestions = rules['plants']
        else:
            suggestions = rules['animals']

    risc = ""
    if data.get('status') is not None:
        if data['status'] == "Risc Scazut":
            risc = "/static/images/Lc.jpg"
        elif data['status'] == "Aproape de pericol":
            risc = "/static/images/Nt.jpg"
        elif data['status'] == "Vulnerabil":
            risc = "/static/images/Vu.jpg"
        elif data['status'] == "In pericol":
            risc = "/static/images/En.jpg"
        elif data['status'] == "Critic":
            risc = "/static/images/Cr.jpg"
        elif data['status'] == "Extinct in salbaticie":
            risc = "/static/images/Ew.jpg"
        elif data['status'] == "Extint":
            risc = "/static/images/Ex.jpg"
    
    if len(risc) > 0:
        risc = f"<img style = \"width:100px; height:100px; \" src = \"{risc}\">" 
    
    
    if len(suggestions) > 0:
        suggestions = f"""
            <br>
            <p align=center style = "font-size:30px;">Sugestii</p>
            <ul>
                <li><p>{suggestions[0]}</p></li>
                <li><p>{suggestions[1]}</p></li>
                <li><p>{suggestions[2]}</p></li>
            </ul>
            <br>
        """
    
    
    html = f'''  
    <div class = "item_second" id = "info">
         <div class="wrapper">
            <div align = right class= "item_first">
                {title}
                {risc}
            </div>
            
            <div class = "item_second">
                 <a href="javascript:void(0)" class="infocbtn prevent-select" onclick="closeInfo()">&times;</a>
            </div>
        </div>

        <p align = left style = "width: 70%">
        {data['description']}
        
        </p>
        
        
        {suggestions}
        
        <div class="slideshow-container">
    
            <div class="mapSlides" width = 50%>
                <img src="{data['images']}/1.jpg" class = "resize">
            </div>
            <div class="mapSlides" width = 50%>
                <img src="{data['images']}/2.jpg" class = "resize">
            </div>
            <div class="mapSlides" width = 50%>
                <img src="{data['images']}/3.jpg" class = "resize">
            </div>
        </div>
        <br>
        
            <div style="text-align:center">
            <span class="dot" onclick="currentSlide(1)"></span>
            <span class="dot" onclick="currentSlide(2)"></span>
            <span class="dot" onclick="currentSlide(3)"></span>
        
        
        </div>
        
    </div>
    </div>
    </div>

    '''
    return html


def species_entry():
    
    args = request.args
    
    mrk = None
    
    if args.get('name') is not None:
        
        name = args.get('name')
        
        for marker in marker_list:
            name_mrk = marker['name']
            if name_mrk == name:
                    mrk = marker
        
        return format_data(mrk)

        
    return render_template('species.html', list=marker_list)
    
if __name__ == '__main__':

    normal_layer = folium.TileLayer(name="Filters", no_wrap=True)
    
    map = folium.Map(
        width = "75%",
        height = "600px",
        location = [45.96268191714687, 25.891383244726377],
        zoom_start = 6.5,
        max_bounds = True,    
        tiles=normal_layer
    )
    
    click_template = """{% macro script(this, kwargs) %}
                        var {{ this.get_name() }} = L.marker(
                            {{ this.location|tojson }},
                            {{ this.options|tojson }}
                            ).addTo({{ this._parent.get_name() }}).on('click', onClick);
                        {% endmacro %}"""

    Marker._template = Template(click_template)

                        
    click_template_p = """{% macro script(this, kwargs) %} 
                          var {{ this.get_name() }} = L.polygon(
                          {{ this.locations|tojson }},
                          {{ this.options|tojson }}
                          ).addTo({{ this._parent.get_name() }}).on('click', onClick);
                          {% endmacro %}"""
    
    folium.Polygon._template = Template(click_template_p)
    
    rules = json.load(open("data/recommendations/recomendations.json", encoding="utf8"))
    
    animal_group = folium.FeatureGroup(name="Animal Species", color='brown')
    plant_group = folium.FeatureGroup(name="Plant Species", color='plant')
    fish_group = folium.FeatureGroup(name="Fish Species", color='blue')
    reservs_group = folium.FeatureGroup(name="Rezervatii Naturale", color='gray')
    
    for j_file in glob.glob("data/protected_species/*.json"):
        if j_file.rfind('template') == -1:
            f = open(j_file, encoding = "utf8")
            js = json.load(f)
            i = 0
            
            spec = None
            
            while i < len(js['location']):
                if js['type'] == 'Animal':
                    spec = folium.Marker(location = js['location'][i], tooltip = js['name'], name = js['name'],icon = folium.CustomIcon('static/images/pawprint.png',icon_size=(45 , 48)))
                    animal_group.add_child(spec)
                elif js['type'] == 'Fish':
                    spec = folium.Marker(location = js['location'][i], tooltip = js['name'], name = js['name'],icon = folium.CustomIcon('static/images/acvatic.png',icon_size=(45 , 48)))
                    fish_group.add_child(spec)
                elif js['type'] == 'Plants':
                    spec = folium.Marker(location = js['location'][i], tooltip = js['name'], name = js['name'],icon = folium.CustomIcon('static/images/frunza.png',icon_size=(45 , 48)))
                    plant_group.add_child(spec)
                i+=1
            
            
            marker_list.append(js)
            
            f.close()
            
    
    
    map.add_child(animal_group)
    map.add_child(plant_group)
    map.add_child(fish_group)
    map.add_child(reservs_group)
    
    folium.map.LayerControl('topright', collapsed = True,).add_to(map)
    
    searchnav = Search(
        layer=reservs_group,
        placeholder="Search a species or location",
        geom_type="Polygon",
        collapsed=True,
        search_label="name",
    ).add_to(map)

    
    for j_file in glob.glob("data/reservations/*.json"):
        if j_file.rfind('template') == -1:
            f = open(j_file, encoding="utf8")
            js = json.load(f)
            
            poly = folium.Polygon(locations= js['area'], color='green', weight=1, fill_color="light_blue", fill_opacity=0.3, fill=True, tooltip=js['name'], name=js['name']).add_to(reservs_group)
            
            area_list.append(js)
            
            f.close()
    
        
    
    app.run(debug=True)