function openNav() {
    document.getElementById("SideNav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}
  
function closeNav() {
    document.getElementById("SideNav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}

function closeInfo(){
    document.getElementById("info").remove();
    document.getElementById("map_div").classList.remove('item_first');
    document.getElementById("map_div").classList.add('no_class')
}