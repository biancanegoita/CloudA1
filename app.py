from flask import Flask, render_template, request, redirect
from google.cloud import datastore

app = Flask(__name__)
datastore_client = datastore.Client()

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)

def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times

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

@app.route('/', methods=['GET','POST'])

def index():
    store_time(datetime.datetime.now())
    times = fetch_times(10)
    return render_template('login.html')
    # if request.method == 'POST':
    #     id = request.form['ID']
    #     pwd = request.form['password']
    #     if not id or not pwd:
    #         msg == "ID or passoword invalid"
    #         return render_tmeplate('login.html',message = msg)
    #     else:
    #         return redirect('/forum', id=id)
    # else:
    #     return render_template('login.html')

@app.route('/login', methods=['GET','POST'])

def login(id,password):
    if request.method == 'POST':
        return render_template('index.html')
        # query = datastore_client.query(kind='user')
        # query.order = ['id']
        # query1 = datastore_client.query(kind='user')
        # query.order = ['password']
        # id = query.fetch(id=id)
        # password = query.fetch(pwd = passoword)
def fetch_user(limit):
    query = datastore_client.query(kind='user')
    user = list (query.fetch(limit = limit))
    return user


@app.route('/register', methods=['GET','POST'])

def register():
    return render_template('register.html')

@app.route('/forum', methods=['GET','POST'])
    
def forum():
    return render_template('forum.html', posts=all_posts)

if __name__ == "__main__":
    app.run(host='120.0.0.1', port=8080,debug=True)

