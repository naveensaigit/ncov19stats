function isTouchDevice() {  
    try {  
      document.createEvent("TouchEvent");  
      return true;  
    } catch (e) {  
      return false;  
    }  
}

function changePiePlot(statename)
{
    $.getJSON("https://api.covid19india.org/data.json",function(data) {
        api=data.statewise;
        var values=[];

        for(var i=0;i<api.length;i++)
        {
            if(api[i]["state"]===statename)
            {
                values=[parseInt(api[i]["active"]),parseInt(api[i]["recovered"]),parseInt(api[i]["deaths"])];
                break;
            }
        }
        var data=JSON.parse($('#33572').text());
        var d=data["38402553-353d-44d8-9c4c-79ff3ea567eb"]["roots"]["references"];
        var sm=values.reduce(function(a,b){return a+b});
        for(var i=1;i<d.length;i++)
        {
            if(d[i]["type"]=="ColumnDataSource")
            {
                d[i]["attributes"]["data"]["values"]=values;
                d[i]["attributes"]["data"]["angle"]=values.map(x=> x*2*Math.PI/sm);
            }
        }
        $('#6422f39e-518d-4907-8d9c-32e446ce7405').html('');
        data["38402553-353d-44d8-9c4c-79ff3ea567eb"]["roots"]["references"]=d;

        $('#33572').text(JSON.stringify(data));
        showPiePlot();
    });
}

function showPiePlot(){
    (function() {
        var fn = function() {
            Bokeh.safely(function() {
            (function(root) {
                function embed_document(root) {
                
                var docs_json = document.getElementById("33572").textContent;
                var render_items = [{"docid":"38402553-353d-44d8-9c4c-79ff3ea567eb","roots":{ "33487" :["6422f39e-518d-4907-8d9c-32e446ce7405"]}}];
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

function changeRPlot(statename,r0)
{
    r=r0[statename];
    var data=JSON.parse($("#32942").text());
    var d=data["c7fc271e-1eeb-42fe-a3b0-443965f537bb"]["roots"]["references"];
    for(var i=0;i<d.length;i++)
    {
        if(d[i]["type"]=="ColumnDataSource")
        {
            d[i]["attributes"]["data"]["r0"]=r;
            break;
        }
    }
    data["c7fc271e-1eeb-42fe-a3b0-443965f537bb"]["roots"]["references"]=d;
    $("#a74704f6-967f-42e2-b90f-c8d724de2845").text('');
    $("#32942").text(JSON.stringify(data));
    showRPlot();
}
function showRPlot()
{
    (function() {
        var fn = function() {
          Bokeh.safely(function() {
            (function(root) {
              function embed_document(root) {
                
              var docs_json = document.getElementById('32942').textContent;
              var render_items = [{"docid":"c7fc271e-1eeb-42fe-a3b0-443965f537bb","roots":{"32701":"a74704f6-967f-42e2-b90f-c8d724de2845"}}];
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

function changeDoubPlot(statename,drate)
{
    drate=drate[statename];
    conf=drate[0];
    rec=drate[1];
    dec=drate[2];

    var data=JSON.parse($("#32266").text());
    var d=data["7f6ae0d0-16dc-45b6-8b9d-fecbe7d8be20"]["roots"]["references"];
    for(var i=0;i<d.length;i++)
    {
        if(d[i]["type"]=="ColumnDataSource")
        {
            d[i]["attributes"]["data"]["conf"]=conf;
            d[i]["attributes"]["data"]["rec"]=rec;
            d[i]["attributes"]["data"]["dec"]=dec;
            break;
        }
    }
    data["7f6ae0d0-16dc-45b6-8b9d-fecbe7d8be20"]["roots"]["references"]=d;
    $("#68ecc955-4a7f-4502-bd5a-45e4730d62f1").text('');
    $("#32266").text(JSON.stringify(data));
    showDoubPlot();
}

function showDoubPlot()
{
    (function() {
        var fn = function() {
          Bokeh.safely(function() {
            (function(root) {
              function embed_document(root) {
                
              var docs_json = document.getElementById('32266').textContent;
              var render_items = [{"docid":"7f6ae0d0-16dc-45b6-8b9d-fecbe7d8be20","roots":{"32037":"68ecc955-4a7f-4502-bd5a-45e4730d62f1"}}];
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

function posDoubPlot()
{
    var x=document.getElementById('doubplot');
    if($(window).width()>1000)
    {
        x.style.marginLeft=String(0.7*$(window).width()-110)+"px";
    }
    else if($(window).width()>630)
    {
        x.style.marginLeft=String(($(window).width()-500)/2)+"px";
    }
    else
    x.style.marginLeft="10px";
}

function replaceText(){
    if($(window).width()<=430)
    {
        var x=document.getElementsByClassName('box');
        for(var i=0;i<x.length;i++)
        {
            x[i].innerText=x[i].innerText.replace('Confirmed','Conf.');
            x[i].innerText=x[i].innerText.replace('Active','Act.');
            x[i].innerText=x[i].innerText.replace('Recovered','Rec.');
            x[i].innerText=x[i].innerText.replace('Deceased','Dec.');
            x[i].innerText=x[i].innerText.replace('Recovery','Rec.');
            x[i].innerText=x[i].innerText.replace('Mortality','Mort.');
            x[i].innerText=x[i].innerText.replace('Increase','Inc.');
            x[i].innerText=x[i].innerText.replace('Recoveries','Rec.');
            x[i].innerText=x[i].innerText.replace('Distribution','Dist.');
            x[i].innerText=x[i].innerText.replace('Doubling','Doub.');
        }
    }
}

function changeStat(statename,x,drate,grate)
{
    var arr=x[statename];
    grate=grate[statename];
    drate=drate[statename];
    
    var st=`<h2 style="text-align: center;">Key Stats</h2>

    <div id="total">
    <div class="box" style="font-weight:600;grid-row:1;grid-column: 1;color:rgb(255, 123, 0);background-color:rgba(255, 123, 0,0.2); ">
        Confirmed<br>${arr[0][0]}<br>(+${arr[0][1]})
    </div>
    <div class="box" style="font-weight:600;grid-row:1;grid-column: 2;color:rgb(255, 0, 0);background-color:rgba(255, 0, 0,0.2); ">
        Active<br>${arr[1][0]}<br><br>
    </div>
    <div class="box" style="font-weight:600;grid-row:1;grid-column: 3;color:rgb(50,205,50);background-color:rgba(50,205,50,0.2); ">
        Recovered<br>${arr[2][0]}<br>(+${arr[2][1]})
    </div>
    <div class="box" style="font-weight:600;grid-row:1;grid-column: 4;color:rgb(77, 75, 75);background-color:rgba(77, 75, 75,0.2); ">
        Deceased<br>${arr[3][0]}<br>(+${arr[3][1]})
    </div>

    <div class="box" style="font-weight:600;grid-row:2;grid-column: 1;color:rgb(0, 119, 255);background-color:rgba(0, 119, 255,0.2);">
        Cases<br>Distribution
    </div>
    <div class="box" style="font-weight:600;grid-row:2;grid-column: 2;color:rgb(0, 119, 255);background-color:rgba(0, 119, 255,0.2);">
        Active<br>${Math.round((arr[1][0]*100/arr[0][0]+Number.EPSILON)*100)/100}%
    </div>
    <div class="box" style="font-weight:600;grid-row:2;grid-column: 3;color:rgb(0, 119, 255);background-color:rgba(0, 119, 255,0.2);">
        Recovery<br>Rate<br>${Math.round((arr[2][0]*100/arr[0][0]+Number.EPSILON)*100)/100}%
    </div>
    <div class="box" style="font-weight:600;grid-row:2;grid-column: 4;color:rgb(0, 119, 255);background-color:rgba(0, 119, 255,0.2);">
        Mortality<br>Rate<br>${Math.round((arr[3][0]*100/arr[0][0]+Number.EPSILON)*100)/100}%
    </div>

    <div class="box" style="font-weight:600;grid-row:3;grid-column: 1;color:rgb(140, 0, 255);background-color:rgba(140, 0, 255,0.2);">
        Increase<br>Rates
    </div>
    <div class="box" style="font-weight:600;grid-row:3;grid-column: 2;color:rgb(140, 0, 255);background-color:rgba(140, 0, 255,0.2);">
        Confirmed<br>${Math.round((grate[0][0]+Number.EPSILON)*1000)/1000}%<br>&Delta;${Math.round((grate[0][1]+Number.EPSILON)*1000)/1000}%
    </div>
    <div class="box" style="font-weight:600;grid-row:3;grid-column: 3;color:rgb(140, 0, 255);background-color:rgba(140, 0, 255,0.2);">
        Recovered<br>${Math.round((grate[1][0]+Number.EPSILON)*1000)/1000}%<br>&Delta;${Math.round((grate[1][1]+Number.EPSILON)*1000)/1000}%
    </div>
    <div class="box" style="font-weight:600;grid-row:3;grid-column: 4;color:rgb(140, 0, 255);background-color:rgba(140, 0, 255,0.2);">
        Deceased<br>${Math.round((grate[2][0]+Number.EPSILON)*1000)/1000}%<br>&Delta;${Math.round((grate[2][1]+Number.EPSILON)*1000)/1000}%
    </div>

    <div class="box" style="font-weight:600;grid-row:4;grid-column: 1;color:rgb(255, 0, 170);background-color:rgba(255, 0, 179,0.2);">
        Doubling<br>Rates<br>(in days)
    </div>
    <div class="box" style="font-weight:600;grid-row:4;grid-column: 2;color:rgb(255, 0, 179);background-color:rgba(255, 0, 179,0.2);">
        Confirmed<br>${drate[0][drate[0].length-1]}<br>&Delta;${drate[0][drate[0].length-1]-drate[0][drate[0].length-2]}
    </div>
    <div class="box" style="font-weight:600;grid-row:4;grid-column: 3;color:rgb(255, 0, 179);background-color:rgba(255, 0, 179,0.2);">
        Recoveries<br>${drate[1][drate[1].length-1]}<br>&Delta;${drate[1][drate[1].length-1]-drate[1][drate[1].length-2]}
    </div>
    <div class="box" style="font-weight:600;grid-row:4;grid-column: 4;color:rgb(255, 0, 179);background-color:rgba(255, 0, 179,0.2);">
        Deaths<br>${drate[2][drate[2].length-1]}<br>&Delta;${drate[2][drate[2].length-1]-drate[2][drate[2].length-2]}
    </div>

    </div>`;
    $("#stat").html(st);
    replaceText();
}

function disableToolBar()
{
  console.log('IN');
  $('#a74704f6-967f-42e2-b90f-c8d724de2845').html('');
  data=JSON.parse($('#32942').text());
  d=data["c7fc271e-1eeb-42fe-a3b0-443965f537bb"]["roots"]["references"];

  for(var i=1;i<d.length;i++)
    if(d[i]["type"]=="Toolbar")
        d[i]["attributes"]["active_drag"]=null;
  data["c7fc271e-1eeb-42fe-a3b0-443965f537bb"]["roots"]["references"]=d;
  $('#32942').text(JSON.stringify(data));
  showRPlot();

  $('#68ecc955-4a7f-4502-bd5a-45e4730d62f1').html('');
  data=JSON.parse($('#32266').text());
  d=data["7f6ae0d0-16dc-45b6-8b9d-fecbe7d8be20"]["roots"]["references"];

  for(var i=1;i<d.length;i++)
    if(d[i]["type"]=="Toolbar")
        d[i]["attributes"]["active_drag"]="None";
  data["7f6ae0d0-16dc-45b6-8b9d-fecbe7d8be20"]["roots"]["references"]=d;
  $('#32266').text(JSON.stringify(data));
  showDoubPlot();
}

$(document).ready(function(){

    //Doubling Plot
    var st=$('#32266').text();
    st=st.split("&#39;").join('"');
    $('#32266').text(st);

    //R0 Plot
    var st=$('#32942').text();
    st=st.split("&#39;").join('"');
    $('#32942').text(st);
    posDoubPlot();
    //Pie Plot
    report('Total');
    replaceText();

    if(isTouchDevice())
    setTimeout(disableToolBar,0.001);
});

$(window).resize(function(){
    posDoubPlot();
    replaceText();
});