function onClick(e){
    var parent = e.parentElement;
    
  for (const child of parent.children) {
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
            console.log("hello");
          }
      })
    }
  }
}