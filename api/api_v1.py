from flask import Flask, jsonify, make_response, request, abort, url_for
import json
import sqlite3

def home_index():
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully")
    api_list=[]
    cursor = conn.execute("SELECT version, buildtime, links, methods from apirelease")

    for row in cursor:
        a_dict = {}
        a_dict['version'] = row[0]
        a_dict['buildtime'] = row[1]
        a_dict['links'] = row[2]
        a_dict['methods'] = row[3]
        api_list.append(a_dict)

    conn.close()
    return jsonify({'api_version': api_list}), 200

def list_users():
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully")
    api_list=[]
    cursor = conn.execute("SELECT id, full_name, username, email, password from users")
    for row in cursor:
        a_dict = {}
        a_dict['id'] = row[0]
        a_dict['name'] = row[1]
        a_dict['username'] = row[2]
        a_dict['email'] = row[3]
        a_dict['password'] = row[4]
        api_list.append(a_dict)
    conn.close()
    return jsonify({'user_list': api_list})

def list_user(user_id):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully")
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT username, full_name, email, password, id from users where id=?",(user_id,))
    data = cursor.fetchall()
    if len(data) != 0:
        user = {}
        user['username'] = data[0][0]
        user['name'] = data[0][1]
        user['email'] = data[0][2]
        user['password'] = data[0][3]
        user['id'] = data[0][4]
    conn.close()
    return jsonify(user)

def add_user(new_user):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully")
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where username=? or email=?",(new_user['username'],new_user['email']))
    data = cursor.fetchall()

    if len(data) != 0:
        abort(409)
    else:
        cursor.execute("insert into users (username, email, password, full_name) values(?,?,?,?)", (new_user['username'],new_user['email'], new_user['password'], new_user['name']))
        conn.commit()
        return "Success"
    
    conn.close()
    return jsonify(a_dict)

def del_user(del_user):
    conn = sqlite3.connect('mydb.db')
    print("Opened database successfully")
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where username=? ",
    (del_user,))
    data = cursor.fetchall()
    print ("Data" ,data)

    if len(data) == 0:
        abort(404)
    else:
        cursor.execute("delete from users where username==?", (del_user,))
        conn.commit()
        return "Success"

def upd_user(user):
    conn = sqlite3.connect('mydb.db')
    print("Opened database successfully")
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where id=? ",(user['id'],))
    data = cursor.fetchall()
    print (data)
    if len(data) == 0:
        abort(404)
    else:
        key_list=user.keys()
        for i in key_list:
            if i != "id":
                print (user, i)
                # cursor.execute("UPDATE users set {0}=? where id=? ", (i, user[i], user['id']))
                cursor.execute("""UPDATE users SET {0} = ? WHERE id = ?""".format(i), (user[i], user['id']))
                conn.commit()
    return "Success"