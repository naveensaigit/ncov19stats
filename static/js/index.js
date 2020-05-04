function changeText(scwth)
{
    var x=document.getElementById('stategrid').children;
    if(scwth<450)
    {
        x[1].innerHTML='Conf.';
        x[2].innerHTML='Act.';
        x[3].innerHTML='Rec.';
        x[4].innerHTML='Dec.';
    }
    else
    {
        x[1].innerHTML='Confirmed';
        x[2].innerHTML='Active';
        x[3].innerHTML='Recovered';
        x[4].innerHTML='Deceased';
    }
}
$(document).ready(function(){
    changeText($(window).width());
});
$(window).resize(function() {
    changeText($(window).width());
});