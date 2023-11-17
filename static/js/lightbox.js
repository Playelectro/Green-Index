function onClick(e){
    var parent = e.parentElement;
    
  for (child of parent.children) {
    if(child.className == "container"){
        var name = child.children[0].textContent;
        $.ajax({
          url: '',
          type: 'get',
          contentType: 'application/json',
          data: {
              name : name
          },
          success: function(response){
            update_page(response);
          }
      })
    }
  }
}

function update_page(response){
  var prev = document.getElementById("info");
  if(prev != null){
      prev.parentNode.removeChild(prev);
  }
  
  var el = document.getElementById('wrapper');
  var tmp = document.getElementsByClassName('no_class')[0];

  tmp.style.display="none";
  
  var aux = document.createElement('template');
  response = response.trim();
  aux.innerHTML = response;
  el.appendChild(aux.content.firstChild);
}

function closeInfo(){
  document.getElementById("info").remove();

  var tmp = document.getElementsByClassName('no_class')[0];

  tmp.style.display="block";
}

function openNav() {
  document.getElementById("SideNav").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("SideNav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}
