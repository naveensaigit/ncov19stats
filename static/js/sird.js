function isTouchDevice() {  
    try {  
      document.createEvent("TouchEvent");  
      return true;  
    } catch (e) {  
      return false;  
    }  
  }

function changeText(){
    if($(window).width()<500)
    {
        var x=document.getElementsByClassName('pred');
        for(var i=0;i<x.length;i++)
        x[i].innerText='Pred.';
        var x=document.getElementsByClassName('act');
        for(var i=0;i<x.length;i++)
        x[i].innerText='Act.';
    }
    else
    {
        var x=document.getElementsByClassName('pred');
        for(var i=0;i<x.length;i++)
        x[i].innerText='Predicted';
        var x=document.getElementsByClassName('act');
        for(var i=0;i<x.length;i++)
        x[i].innerText='Actual';
    }
}

function center()
{
    var x=document.getElementById('long');
    x.style.marginLeft=String(($(window).width()-$('#long').width())/2)+"px";
    var x=document.getElementById('points');
    x.style.marginLeft=String(($(window).width()-$('#long').width())/2)+"px";
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
}

function showLongTermPlot()
{
  (function() {
    var fn = function() {
      Bokeh.safely(function() {
        (function(root) {
          function embed_document(root) {
            
          var docs_json = document.getElementById('23161').textContent;
          var render_items = [{"docid":"f73282ce-168b-4fdc-a946-43d7c124e558","roots":{"22908":"5c25aeba-19f5-4cb0-a854-c436629e11c7"}}];
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

  $('#5c25aeba-19f5-4cb0-a854-c436629e11c7').html('');
  data=JSON.parse($('#23161').text());
  d=data["f73282ce-168b-4fdc-a946-43d7c124e558"]["roots"]["references"];

  for(var i=1;i<d.length;i++)
    if(d[i]["type"]=="Toolbar")
        d[i]["attributes"]["active_drag"]="None";
  data["f73282ce-168b-4fdc-a946-43d7c124e558"]["roots"]["references"]=d;
  $('#23161').text(JSON.stringify(data));
  showLongTermPlot();
}

$(document).ready(function(){
    changeText();
    center();
});

$(window).resize(function(){
    changeText();
    center();
});