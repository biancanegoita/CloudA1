import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.run(host='https://clouda1-309323.ue.r.appspot.com/', port=8080, debug=True)
all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is the content of post 1',
        'author':'s38060120'
    },
    {
        'title': 'Post 2',
        'content': 'This is the content of post 2',
    },
    {
        'title': 'Post 3',
        'content': 'This is the content of post 3',
    },
    {
        'title': 'Post 4',
        'content': 'This is the content of post 4',
    },
    {
        'title': 'Post 4',
        'content': 'This is the content of post 4',
    },
    {
        'title': 'Post 5',
        'content': 'This is the content of post 5',
    },
    {
        'title': 'Post 6',
        'content': 'This is the content of post 6',
    },
    {
        'title': 'Post 7',
        'content': 'This is the content of post 7',
    }

]

@app.route('/login', methods=['GET','POST'])

def login():
    if request.method == 'POST':
        id = request.form['ID']
        pwd = request.form['password']
        if not id or not pwd:
            msg == "ID or passoword invalid"
            return render_tmeplate('login.html',message = msg)
        else:
            return redirect('/forum', id=id)
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET','POST'])

def register():
    return render_template('register.html')

@app.route('/forum', methods=['GET','POST'])
    
def forum():
    return render_template('forum.html', posts=all_posts)

if __name__ == "__main__":
    app.run(debug=True)
