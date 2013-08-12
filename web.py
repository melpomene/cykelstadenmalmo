#!/usr/bin/env python
# encoding: utf-8

import sqlite3
from datetime import datetime, timedelta
from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
    conn = sqlite3.connect('db.sql')
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
    <style>
        #red {
            color: red;
        }
    </style>
    </head>

    <body style="text-align:center">

        <h1>Cykelstaden Malmö</h1>
        <h3>Antal olyckor den här månaden: <font id="red">%d</font></h3>
        <p><a href="/list/">?</a></p>
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
    c.execute('SELECT tweet_id, tweet, time, url from tweets ORDER BY tweet_id')
    res = []
    for row in c:
        res.append( (row[0], row[1], row[2], row[3]))

    start_html = u"""

<html>
    <head>
    <style>
        #red {
            color: red;
        }
        #center {
            text-align:center;
        }
    </style>
    </head>

    <body >

        <a href="/"><h1 style="text-align:center">Cykelstaden Malmö</h1></a>
        <p>Cykelolyckor i Malmö raporterade av polisen de senaste 31 dagarna:</p>
        <ul>
"""
    l = ""
    for row in res: 
        l += u"<li><a href='%s'>%s</a></li>" % (row[3], row[1][:80]+ "...")
    end_html = u"""
    </ul>

    <p>
        Jag är en cyklist i Malmö, vill ni kontakta mig når ni mig lättast på <a href="https://twitter.com/kejsarmakten">Twitter</a> eller <a href="http://blog.kejsarmakten.se/">här</a>
    </p>
    <center><img width="150px" class="center" src="http://i.imgur.com/kTRS6py.png" /></center>
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
"""
    return start_html + l + end_html


if __name__ == "__main__":
    app.debug = True
    app.run()
