function menuChange(scwth)
{
    var x=document.getElementById('navbar').children;
    if(scwth<450)
    {
        x[0].innerHTML='<i class="material-icons" style="vertical-align:sub;font-size:150%;">home</i>';
        x[1].innerHTML='SIRD';
        x[4].innerHTML='<i class="material-icons" style="vertical-align:sub;font-size:150%;">help_outline</i>';
    }
    else
    {
        x[0].innerHTML='Home';
        x[1].innerHTML='SIRD Model';
        x[4].innerHTML='About';
    }
}

$(document).ready(function(){
    menuChange($(window).width());
});
$(window).resize(function() {
    menuChange($(window).width());
  });