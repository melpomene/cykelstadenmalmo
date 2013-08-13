Cykelstaden Malmö
=================

Ibland känns det lite lätt livsfarligt att ta sig genom Malmö på cykel.
Hackade ihop en liten webbapp för att dokumentera hur många cykelolycker som rapporteras in i månaden.

Den är live här [cykelstaden.kejsarmakten.se](http://cykelstaden.kejsarmakten.se/).

Består av två bitar, en webbapp som är skriven med Flask, samt en crawler som hämtar ner infromation från Malmö polisens Twitter.

Om någon orkar lägga på lite CSS hade det varit trevlig, forka på!

Installation
------------

Kräver följande python paket

* flask
* python-twitter

Sqlite3 databasen har följande utseende:

    CREATE TABLE tweets (id INTEGER PRIMARY KEY NOT NULL, tweet TEXT, time DATETIME DEFAULT CURRENT_TIMESTAMP, tweet_id INTEGER, url TEXT, adress TEXT);

Frågor?
-------

Skicka mig ett mail, ni hittar adressen till vänster eller i på min [blogg](http://blog.kejsarmakten.se/about.html). 
