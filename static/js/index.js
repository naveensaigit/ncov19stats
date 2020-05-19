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

function changeMap(status)
{
  var states={'Andaman and Nicobar Islands': [0,0,0,0],  'Arunachal Pradesh': [0,0,0,0],  'Assam': [0,0,0,0],  'Bihar': [0,0,0,0],  'Chandigarh': [0,0,0,0],  'Chhattisgarh': [0,0,0,0],
  'Dadra and Nagar Haveli': [0,0,0,0],  'Daman and Diu': [0,0,0,0],  'Goa': [0,0,0,0],  'Gujarat': [0,0,0,0],  'Haryana': [0,0,0,0],  'Himachal Pradesh': [0,0,0,0],  'Jharkhand': [0,0,0,0],
  'Karnataka': [0,0,0,0],  'Kerala': [0,0,0,0],  'Lakshadweep': [0,0,0,0],  'Madhya Pradesh': [0,0,0,0],  'Maharashtra': [0,0,0,0],  'Manipur': [0,0,0,0],  'Meghalaya': [0,0,0,0],  'Mizoram': [0,0,0,0],
  'Nagaland': [0,0,0,0], 'Delhi': [0,0,0,0],  'Puducherry': [0,0,0,0],  'Punjab': [0,0,0,0],  'Rajasthan': [0,0,0,0],  'Sikkim': [0,0,0,0],  'Tamil Nadu': [0,0,0,0],  'Telangana': [0,0,0,0],  'Tripura': [0,0,0,0],
  'Uttar Pradesh': [0,0,0,0], 'Uttarakhand': [0,0,0,0],  'West Bengal': [0,0,0,0],  'Odisha': [0,0,0,0],  'Andhra Pradesh': [0,0,0,0],  'Jammu and Kashmir': [0,0,0,0],  'Ladakh': [0,0,0,0]};
  var indpal={"Confirmed":[0,["#ffe3bd","#ffd8a3","#ffc77a","#ffba5c","#ffaf42","#ffa933","#ffa121","#ff9300"]],
              "Active":[1,["#fff0f0", "#ffdbdb", "#ffd4d4", "#ff9696", "#ff6666", "#fa4848", "#ff3636", "#ff0000"]],
              "Recovered":[2,["rgba(0,195,0,0.125)","rgba(0,195,0,0.25)","rgba(0,195,0,0.375)","rgba(0,195,0,0.5)","rgba(0,195,0,0.625)","rgba(0,195,0,0.75)","rgba(0,195,0,0.875)","rgba(0,195,0,1)"]],
              "Deceased":[3,["#d2d4d2","#bbbdbb","#a4a6a4","#8d8f8d","#757875","#646664","#525452","#414241"]]
              }
  var ind=indpal[status][0];
  $.getJSON("https://api.covid19india.org/data.json",function(data) {
        api=data.statewise;
        for(var i=1;i<api.length;i++)
        {    
          if(api[i]["state"]=="State Unassigned")
          continue;
          if(api[i]["state"]!="Dadra and Nagar Haveli and Daman and Diu")
          {
            states[api[i]["state"]][0]+=api[i]["confirmed"];
            states[api[i]["state"]][1]+=api[i]["active"];
            states[api[i]["state"]][2]+=api[i]["recovered"];
            states[api[i]["state"]][3]+=api[i]["deaths"];
          }
          else
          {
            states["Dadra and Nagar Haveli"][0]+=api[i]["confirmed"];
            states["Dadra and Nagar Haveli"][1]+=api[i]["active"];
            states["Dadra and Nagar Haveli"][2]+=api[i]["recovered"];
            states["Dadra and Nagar Haveli"][3]+=api[i]["deaths"];
            states["Daman and Diu"][0]+=api[i]["confirmed"];
            states["Daman and Diu"][1]+=api[i]["active"];
            states["Daman and Diu"][2]+=api[i]["recovered"];
            states["Daman and Diu"][3]+=api[i]["deaths"];
          }
        }
        var val=$.map(states, function(value, key) { return parseInt(value[ind]) });
        data=JSON.parse($("#1936").text());
        var d=data["45e132a7-a530-4d0b-ac49-8357983a6781"]["roots"]["references"];
        val=val.slice(0,37);
        var m=val[0];
        for(var i=1;i<val.length;i++)
          if(m<val[i])
            m=val[i];

        d[26]["attributes"]["data"]["color"]=val;
        d[7]["attributes"]["high"]=m;
        var pal=indpal[status][1];
        d[7]["attributes"]["palette"]=pal;
        d[23]["attributes"]["line_color"]=pal[4];

        data["45e132a7-a530-4d0b-ac49-8357983a6781"]["roots"]["references"]=d;
        $('#1936').text(JSON.stringify(data));
        $('#b2b9fd67-9cc3-418e-833d-21fc86472b98').html('');
        $("#max").text(m);

        var x=document.getElementById("colorbar");
        x.style.background=`linear-gradient(to right,${pal[0]},${pal[1]},${pal[2]},${pal[3]},${pal[4]},${pal[5]},${pal[6]},${pal[7]})`;

        var x=document.getElementById("message");
        x.innerHTML="<i>"+status+" Cases (Click on Confirmed/Active/Recovered/Deceased to change the Heat-Map)</i>";
        showMap();
      }
  );
}

function showMap()
{
  (function() {
    var fn = function() {
      Bokeh.safely(function() {
        (function(root) {
          function embed_document(root) {
            
          var docs_json = document.getElementById('1936').textContent;
          var render_items = [{"docid":"45e132a7-a530-4d0b-ac49-8357983a6781","roots":{"1839":"b2b9fd67-9cc3-418e-833d-21fc86472b98"}}];
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
}

$(document).ready(function(){
    changeText($(window).width());
    var x=document.getElementsByClassName('state');
    for(var i=0;i<5;i++)
    x[i].style.fontWeight="900";
    console.log('tests');
});
$(window).resize(function() {
    changeText($(window).width());
    centerAlignSlider();
});