
import json

rules = json.load(open("data/recommendations/recomendations.json", encoding="utf8"))


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

#
#
#
#
#
#

def format_data_gallery(data):
    
    title = f"<h1>{data['name']}</h1>"


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
        
        <div class="grid-container">
    
            <div class="card" style=" width: 85%">
                <img src="{data['images']}/1.jpg" style="width:100%; height:300px;">
            </div>
            <div class="card" style="width: 85%">
                <img src="{data['images']}/2.jpg" style="width:100%; height:300px;">
            </div>
            <div class="card" style=" width: 85%">
                <img src="{data['images']}/3.jpg" style="width:100%; height:300px;">
            </div>
        </div>
        <br>
        
        </div>
        
    </div>
    </div>
    </div>

    '''
    return html