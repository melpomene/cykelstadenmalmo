#!/usr/bin/env python
# encoding: utf-8

import sqlite3
from datetime import datetime, timedelta
from flask import Flask
app = Flask(__name__)
DB_PATH = 'db.sql' 
@app.route("/")
def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT tweet_id, tweet, time from tweets ORDER BY tweet_id')
    res = []
    for row in c:
        # 2013-08-07 08:33:08
        if datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S" ) > datetime.today() - timedelta(days=31):
            res.append( (row[0], row[1], row[2]))

    amount = len(res)
    html =  """
<html>
    <head>
    <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="static/style.css">
    </head>
    <body style="text-align:center">
        <h1>Cykelstaden Malmö</h1>
        <h3>Antal olyckor den här månaden:</h3>
        <div class="antal">%d</div>
        <a class="btn"  href="/list/">?</a>
          <!-- Piwik -->
    <script type="text/javascript">
      var _paq = _paq || [];
      _paq.push(["setDocumentTitle", document.domain + "/" + document.title]);
      _paq.push(["trackPageView"]);
      _paq.push(["enableLinkTracking"]);

      (function() {
        var u=(("https:" == document.location.protocol) ? "https" : "http") + "://links.kejsarmakten.se/piwik/";
        _paq.push(["setTrackerUrl", u+"piwik.php"]);
        _paq.push(["setSiteId", "1"]);
        var d=document, g=d.createElement("script"), s=d.getElementsByTagName("script")[0]; g.type="text/javascript";
        g.defer=true; g.async=true; g.src=u+"piwik.js"; s.parentNode.insertBefore(g,s);
      })();
    </script>
    <!-- Piwik Image Tracker -->
    <img src="http://links.kejsarmakten.se/piwik/piwik.php?idsite=1&amp;rec=1" style="border:0" alt="" />
    <!-- End Piwik -->
   <!-- End Piwik Code -->  
        
    </body>
</html>
""" % (amount)
    return html

@app.route("/list/")
def list():
    conn = sqlite3.connect('db.sql')
    c = conn.cursor()
    c.execute('SELECT tweet_id, tweet, time, url, adress from tweets ORDER BY tweet_id')
    res = []
    for row in c:
        res.append( (row[0], row[1], row[2], row[3],row[4]))

    start_html = u"""

<html>
    <head>
    <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="/static/style.css">
    <script src="http://codeorigin.jquery.com/jquery-2.0.3.min.js" type="text/javascript"></script> 
    <style>
    html { height: 100% }
      body { height: 100%; margin: 0; padding: 0 }

     #map-canvas { height: 80% }

        #red {
            color: red;
        }
        #center {
            text-align:center;
        }
    </style>
    <script type="text/javascript"
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAw_oiAiVvap_tRxyIzf8aabP1jwPlR0ps&sensor=false">
    </script>
<script type="text/javascript">

google.maps.event.addDomListener(window, 'load', initialize);

function initialize(){

  var geocoder_map;
    var map;
    var markers;
    var address = new Array();
    """
    k = ""
    for row in res:
       k += u"address.push('%s + MalmÃ¶,Sweden');" % (row[4])



    j=u"""
    
    var markersStr;
   
    //set your map options
    var myOptions = {
        //zoom: 13,
        disableDefaultUI: false,
        mapTypeId: google.maps.MapTypeId.HYBRID
    };
   
    //create the new map instance and attach to your DOM element
    var map = new google.maps.Map(document.getElementById("map-canvas"),myOptions);
   
    //create the bound object; used for centering
    var latlngbounds = new google.maps.LatLngBounds();
   
    //new geocoder to convert the addresses to coordinates
    geocoder_map = new google.maps.Geocoder();
    markers = new Array();
   
    //loop through the addresses and add the resulting coordinates to an array
    for(var i=0;i<address.length;i++){
        geocoder_map.geocode( { 'address': address[i]}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                //add marker to the map
                var marker = new google.maps.Marker({
                    map: map, position: results[0].geometry.location
                });
                markers.push(results[0].geometry.location);
            }
            else {
                alert("Geocode for "+address+" was not successful for the following reason: " + status);
            }
        });
    }
   
    // wait 500ms so the array is fully populated
    setTimeout(function(){
        for(var i=1; i < markers.length; i++){
            //add coordinates to the outer bounds of the map
            latlngbounds.extend(markers[i]);    
        }
        //set the center to the bound area and fit the map accordingly
        map.setCenter(latlngbounds.getCenter());
        //map.fitBounds(latlngbounds);
    },500);
};
    
    </script>
    </head>

    <body >

        <a href="/"><h1 style="text-align:center">Cykelstaden Malmö</h1></a>
        <div class="warp" >
        <p>Cykelolyckor i MalmÃ¶ raporterade av polisen de senaste 31 dagarna:</p>
        <ul>
"""
    l = ""
    for row in res:
        l += u"<li class='%s' ><a href='%s'>%s</a></li>" % (row[4],row[3], row[1][:120]+ "...")
    end_html = u"""
    </ul>

    <p>
       Jag är en cyklist i MalmÃ¶. Ni kan nå mig på <a href="https://twitter.com/kejsarmakten">Twitter</a> eller via <a href="http://blog.kejsarmakten.se/">min blogg</a>.
    </p>
  
<div id="map-canvas"/>
    <div id="map-canvas"/>
    <!-- Piwik -->
    <script type="text/javascript">
      var _paq = _paq || [];
      _paq.push(["setDocumentTitle", document.domain + "/" + document.title]);
      _paq.push(["trackPageView"]);
      _paq.push(["enableLinkTracking"]);

      (function() {
        var u=(("https:" == document.location.protocol) ? "https" : "http") + "://links.kejsarmakten.se/piwik/";
        _paq.push(["setTrackerUrl", u+"piwik.php"]);
        _paq.push(["setSiteId", "1"]);
        var d=document, g=d.createElement("script"), s=d.getElementsByTagName("script")[0]; g.type="text/javascript";
        g.defer=true; g.async=true; g.src=u+"piwik.js"; s.parentNode.insertBefore(g,s);
      })();
    </script>
    <!-- Piwik Image Tracker -->
    <img src="http://links.kejsarmakten.se/piwik/piwik.php?idsite=1&amp;rec=1" style="border:0" alt="" />
    <!-- End Piwik -->
    <!-- End Piwik Code --> 

    </div>
    </body>
</html>
"""
    return start_html + k + j + l + end_html


if __name__ == "__main__":
   app.debug = False 
    app.run(host="0.0.0.0") 
