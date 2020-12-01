from flask import Flask, jsonify, make_response, request, abort, url_for
import json
import sqlite3

def list_tweets():
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully")
    api_list=[]
    cursor = conn.execute("SELECT username, body, tweet_time, id from tweets")
    data = cursor.fetchall()
 
    if len(data) != 0:
        for row in data:
            tweets = {}

            tweets['tweetedby'] = row[0]
            tweets['body'] = row[1]
            tweets['timestamp'] = row[2]
            tweets['id'] = row[3]

            api_list.append(tweets)
    else:
        return api_list
    
    conn.close()
    return jsonify({'tweets_list': api_list})

def list_tweet(user_id):
    print (user_id)
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully")
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * from tweets where id=?",(user_id,))
    data = cursor.fetchall()
    print (data)

    if len(data) == 0:
        abort(404)
    else:
        user = {}
        user['id'] = data[0][0]
        user['username'] = data[0][1]
        user['body'] = data[0][2]
        user['tweet_time'] = data[0][3]
        conn.close()
        return jsonify(user)

def add_tweet(new_tweets):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully")
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where username=? ", (new_tweets['username'],))
    data = cursor.fetchall()

    if len(data) == 0:
        abort(404)
    else:
        cursor.execute("INSERT into tweets (username, body, tweet_time) values(?,?,?)",(new_tweets['username'],new_tweets['body'], new_tweets['created_at']))
        conn.commit()
        return "Success"
