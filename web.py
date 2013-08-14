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
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Cykelstaden Malmö - Övervakar cykelolyckor i Malmö</title>
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
    </body>
</html>
""" % (amount)
    return html

@app.route("/list/")
def list():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT tweet_id, tweet, time, url, adress from tweets ORDER BY tweet_id')
    res = []
    for row in c:
        res.append( (row[0], row[1], row[2], row[3],row[4]))

    start_html = u"""

<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="/static/style.css">
    <title>Cykelstaden Malmö - Övervakar cykelolyckor i Malmö</title>
    <style>
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
        var color=["red","green","purple","yellow","blue","gray","orange"," white"]
        var markers, url,geocoder_map;
        var b = new Array(); //lon & lat of addresses
        var address = new Array();

        """
        k = ""
        for row in res:
           k += u"address.push('%s  ,Malmö,Sweden');" % (row[4])

        j=u"""
       
        //new geocoder to convert the addresses to coordinates
        geocoder_map = new google.maps.Geocoder();
        
       
        //loop through the addresses and add the resulting coordinates to an array
        for(var i=0;i<address.length;i++){
            geocoder_map.geocode( { 'address': address[i]}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    
                    b.push(results[0].geometry.location.lat()+","+results[0].geometry.location.lng());
                }
                else {
                    alert("Geocode for "+address+" was not successful for the following reason: " + status);
                }
            });
        }
       
        // wait 500ms so the array is fully populated
        setTimeout(function(){

            for (var i=0;i<address.length;i++){
                markers = markers + "&markers=color:"+color[i]+"|label:" + (i+1) + "|"+ b[i]
                url="http://maps.googleapis.com/maps/api/staticmap?center=södervärn,Malm%C3%B6,sweden&zoom=12&size=640x460&maptype=roadmap%20" + markers +"&scale=1&sensor=false"
            }
            addpic(url);

        },500);
    };

    function addpic(url){

    var elem = document.createElement("img");
    elem.setAttribute("src", url);
    document.getElementById("map-canvas").appendChild(elem);

    }

    </script>
    </head>
    <body >

        <a href="/"><h1 style="text-align:center">Cykelstaden Malmö</h1></a>
        <div class="warp" >
        <p>Cykelolyckor i Malmö raporterade av polisen de senaste 31 dagarna:</p>
        <ul>
"""
    l = ""
    for row in res:
        l += u"<li class='%s' ><a href='%s' target='_blank'>%s</a></li>" % (row[4],row[3], row[1][:120]+ "...")
    end_html = u"""
    </ul>

    <p>
        Jag är en cyklist i Malmö. Ni kan nå mig på <a href="https://twitter.com/kejsarmakten">Twitter</a> eller via <a href="http://blog.kejsarmakten.se/">min blogg</a>.<br />
        Design och karta är fixat av <a href="https://twitter.com/ehsanpo">@ehsanpo</a>, tackar!
    </p>

<div id="map-canvas"/></div>
    <div>
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
    app.debug = True 
    app.run(host="0.0.0.0")

