from flask import Flask, jsonify, make_response, request, abort, url_for, render_template, redirect, session
from time import gmtime, strftime
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import flask
import json
import sqlite3
import random
from api.api_v1 import home_index, list_users, list_user, add_user, del_user, upd_user
from api.api_v2 import list_tweets, list_tweet, add_tweet

# connection to MongoDB Database
connection = MongoClient("mongodb://localhost:27017/")

app = Flask(__name__)
# cookie = flask.request.cookies.get('my_cookie')
app.secret_key = 'aezakmi'
CORS(app)

# Initialize Database
def create_mongodatabase():
    try:
        dbnames = connection.database_names()
        if 'cloud_native' not in dbnames:
            db = connection.cloud_native.users
            db_tweets = connection.cloud_native.tweets
            db_api = connection.cloud_native.apirelease

            db.insert({
            "email": "eric.strom@google.com",
            "id": 33,
            "name": "Eric stromberg",
            "password": "eric@123",
            "username": "eric.strom"
            })

            db_tweets.insert({
            "body": "New blog post,Launch your app with the AWS Startup Kit! #AWS",
            "id": 18,
            "timestamp": "2017-03-11T06:39:40Z",
            "tweetedby": "eric.strom"
            })

            db_api.insert( {
              "buildtime": "2017-01-01 10:00:00",
              "links": "/api/v1/users",
              "methods": "get, post, put, delete",
              "version": "v1"
            })
            db_api.insert( {
              "buildtime": "2017-02-11 10:00:00",
              "links": "api/v2/tweets",
              "methods": "get, post",
              "version": "2017-01-10 10:00:00"
            })
            print ("Database Initialize completed!")
        else:
            print ("Database already Initialized!")
    except:
        print ("Database creation failed!!")


@app.route("/")
def root():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/addname')
def addname():
    if request.args.get('yourname'):
        session['name'] = request.args.get('yourname')
        # And then redirect the user to the main page
        return redirect(url_for('home'))
    else:
        return render_template('home.html', session=session)

@app.route('/clear')
def clearsession():
    session.clear()
    return redirect(url_for('home'))

# @app.route('/set_cookie')
# def cookie_insertion():
#     redirect_to_main = redirect('/')
#     response = current_app.make_response(redirect_to_main )
#     response.set_cookie('cookie_name',value='values')
#     return response

@app.route("/api/v1/info")
def api_v1_info():
    return home_index()

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    
    user = {
        'name': request.json.get('name',""),
        'username': request.json['username'],
        'email': request.json['email'],
        'password': request.json['password'],
        'id': random.randint(1,1000)
    }

    return jsonify({'status': add_user(user)}), 201

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    
    user=request.json['username']
    return jsonify({'status': del_user(user)}), 200

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    if not request.json:
        abort(400)

    user['id']=user_id
    key_list = request.json.keys()
    
    for i in key_list:
        user[i] = request.json[i]

    return jsonify({'status': upd_user(user)}), 200

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
    return list_tweet(id)

@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    
    user_tweet['tweetedby'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['timestamp']=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    user_tweet['id'] = random.randint(1,1000)

    return jsonify({'status': add_tweet(user_tweet)}), 200

@app.route('/adduser')
def adduser():
    return render_template('adduser.html')

@app.route('/addtweets')
def addtweetjs():
    return render_template('addtweets.html')


@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)

@app.errorhandler(409)
def user_found(error):
    return make_response(jsonify({'error': 'Conflict! Record exist'}), 409)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

if __name__ == '__main__':
    create_mongodatabase()
    app.run(host='0.0.0.0', port=5000, debug=True)