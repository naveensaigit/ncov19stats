function isTouchDevice() {  
  try {  
    document.createEvent("TouchEvent");  
    return true;  
  } catch (e) {  
    return false;  
  }  
}

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

//Bokeh Plot variables
var doc_id="e6966378-2024-4dd6-ac89-dc9156ead24c";  //Dict key of script
var script_id="14473";  //Script tag ID
var plot_div_id="2657d1c2-7221-458f-908f-f6bc367374f7";  //Div id of bk-root div
var data_root_id="14120";

function changePlot(cumconf,cumact,cumrec,cumdec,oldconf,oldrec,olddec,newconf,newrec,newdec,dates,x){
  $('#'+plot_div_id).html('');
  data=JSON.parse($('#'+script_id).text());
  d=data[doc_id]["roots"]["references"];

  var dt=new Date();
  dt.setDate(dt.getDate()-1);
  dt.setHours(5);
  dt.setMinutes(30);
  dt.setSeconds(0);
  dt.setMilliseconds(0);
  console.log(dt);
  for(var i=1;i<d.length;i++)
  {
    if(d[i]["type"]=="ColumnDataSource")
      {
        if(d[i]["attributes"]["data"]["cumact"]!=null)
        {
          d[i]["attributes"]["data"]["cumact"]=cumact;
          d[i]["attributes"]["data"]["dispcumact"]=cumact;
        }
        else if(d[i]["attributes"]["data"]["cumrec"]!=null)
        {
          d[i]["attributes"]["data"]["cumrec"]=cumrec;
          d[i]["attributes"]["data"]["newrec"]=newrec;
          d[i]["attributes"]["data"]["oldrec"]=oldrec;
          d[i]["attributes"]["data"]["dispcumrec"]=cumrec;
          d[i]["attributes"]["data"]["dispnewrec"]=newrec;
          d[i]["attributes"]["data"]["dispoldrec"]=oldrec;
        }
        else if(d[i]["attributes"]["data"]["cumconf"]!=null)
        {
          d[i]["attributes"]["data"]["cumconf"]=cumconf;
          d[i]["attributes"]["data"]["newconf"]=newconf;
          d[i]["attributes"]["data"]["oldconf"]=oldconf;
          d[i]["attributes"]["data"]["dispcumconf"]=cumconf;
          d[i]["attributes"]["data"]["dispnewconf"]=newconf;
          d[i]["attributes"]["data"]["dispoldconf"]=oldconf;
        }
        else if(d[i]["attributes"]["data"]["cumdec"]!=null)
        {
          d[i]["attributes"]["data"]["cumdec"]=cumdec;
          d[i]["attributes"]["data"]["newdec"]=newdec;
          d[i]["attributes"]["data"]["olddec"]=olddec;
          d[i]["attributes"]["data"]["dispcumdec"]=cumdec;
          d[i]["attributes"]["data"]["dispnewdec"]=newdec;
          d[i]["attributes"]["data"]["dispolddec"]=olddec;
        }
        d[i]["attributes"]["data"]["dates"]=dates;
        d[i]["attributes"]["data"]["dispdates"]=dates;
        d[i]["attributes"]["data"]["x"]=x;
      }
    if(d[i]["type"]=="DateRangeSlider")
    {
        d[i]["attributes"]["end"]=dt.setMilliseconds(0);
        d[i]["attributes"]["value"]["1"]=dt.setMilliseconds(0);
    }
  }
  data[doc_id]["roots"]["references"]=d;

  $('#'+script_id).text(JSON.stringify(data));
  showPlot();
  console.log('Changed');
}

function showPlot()
{
  (function() {
    var fn = function() {
      Bokeh.safely(function() {
        (function(root) {
          function embed_document(root) {
            
          var docs_json = document.getElementById(script_id).textContent;
          var render_items = [{"docid": [doc_id] ,"roots":{ [data_root_id] :[plot_div_id]}}];
          root.Bokeh.embed.embed_items(docs_json, render_items);
        
          }
          if (root.Bokeh !== undefined) {
            embed_document(root);
          } else {
            var attempts = 0;
            var timer = setInterval(function(root) {
              if (root.Bokeh !== undefined) {
                clearInterval(timer);
                embed_document(root);
              } else {
                attempts++;
                if (attempts > 100) {
                  clearInterval(timer);
                  console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing");
                }
              }
            }, 10, root)
          }
        })(window);
      });
    };
    if (document.readyState != "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  })();
  setTimeout(centerAlignSlider, 300);
}

function centerAlignSlider(){
  var x=document.getElementsByClassName('bk bk-input-group'); 
  for(var i=0;i<x.length;i++)
  x[i].style.marginLeft=String(($('#plots').width()-parseInt(x[0].parentElement.style.width))/2)+"px";
}

function centerDropDown(){
  var x=document.getElementById('table').style.width;
  var y=document.getElementById('drop');
  y.style.marginRight=($(window).width()-(x+461.2))/2;
}

function disableToolBar()
{
  $('#'+plot_div_id).html('');
  data=JSON.parse($('#'+script_id).text());
  d=data[doc_id]["roots"]["references"];

  for(var i=1;i<d.length;i++)
    if(d[i]["type"]=="Toolbar")
        d[i]["attributes"]["active_drag"]="None";
  data[doc_id]["roots"]["references"]=d;
  $('#'+script_id).text(JSON.stringify(data));
  showPlot();
}

$(document).ready(function(){
    changeText($(window).width());
});
$(window).resize(function() {
    changeText($(window).width());
    centerAlignSlider();
});