#!/usr/bin/env python
# encoding: utf-8

import twitter
import sqlite3
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.cfg')

api = twitter.Api(consumer_key=config.get("twitter", "CONSUMER_KEY"),
                    consumer_secret=config.get("twitter", "CONSUMER_SECRET"),
                    access_token_key=config.get("twitter", "access_token_key"),
                    access_token_secret=config.get("twitter", "access_token_secret"))


if __name__ == '__main__':
    
    conn = sqlite3.connect('db.sql')
    c = conn.cursor()
    c.execute('SELECT tweet_id from tweets ORDER BY tweet_id DESC LIMIT 1')
    
    latest_id = c.fetchone()
    if latest_id is None:
        latest_id = [1]
    latest_id = latest_id[0]

    statuses = api.GetUserTimeline(screen_name="polisen_malmo", since_id=int(latest_id))
    if statuses is None:
        print "Nothing new"
        exit()

    for tweet in statuses:
        tweet_id = tweet.id
        tweet_text = tweet.text
        url = tweet.urls[0].url
        lista = tweet.text.split(',')
        adress = lista[2].split('http',1)[0]
        if "cykel" in tweet_text or "cyklist" in tweet_text:
            c.execute('INSERT INTO tweets (tweet, tweet_id, url,adress) VALUES (?, ?, ?, ?)', (tweet_text, tweet_id, url, adress))
            print "JA\t" + tweet_text
        else:
            print "NEJ\t"+tweet_text
    conn.commit()
    conn.close()

            
