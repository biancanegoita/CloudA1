from flask import Flask, render_template, request, redirect, session
from google.cloud import datastore, storage
import datetime


app = Flask(__name__)
datastore_client = datastore.Client()
gcs = storage.Client()
bucket = gcs.get_bucket('imagesclouda1')

entity = datastore.Entity(key=datastore_client.key('user'))
query = datastore_client.query(kind='user')
msg = ["ID or password invalid","user already exists","The old password is incorrect"]
app.secret_key='secret key'

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



@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        id = request.form['ID']
        password = request.form['password']

        query=datastore_client.query(kind='user')
        activeuser = list(query.add_filter('id','=',id).fetch())
        
        #user_name=activeuser[0]['user_name']
        print(activeuser)
        if not activeuser or (activeuser[0]['password']!=password):
            return render_template('login.html', message=msg[0])
        else:
            session['id'] = id
            user_name = activeuser[0]['user_name']
           # msg1 == "we got your info"
            return redirect('/forum')        
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET','POST'])

def register():
    if request.method == 'POST':
        id = request.form['ID']
        password = request.form['password']
        user_name = request.form['user_name']
        image = request.files['filename']
        user_exists = list(query.add_filter('id','=',id).fetch())
        user_exists1 = list(query.add_filter('user_name','=',user_name).fetch())
        
        if user_exists or user_exists1:
            return render_template('register.html', message = msg[2])
        else:
            if image:
                blob = bucket.blob(image.filename)
                blob.upload_from_string(
                    image.read(),
                    content_type=image.content_type
                )
                image_url = blob.public_url
                entity = datastore.Entity(datastore_client.key('user'))
                entity.update(
                    {
                        "id":id,
                        "user_name":user_name,
                        "password":password,
                        "image_url":image_url,
                    }
                )
                datastore_client.put(entity)
                return redirect('/')
    else:
        return render_template('register.html')

@app.route('/forum', methods=['GET','POST'])
    
def forum():
    query = datastore_client.query(kind='user')
    current_user= list(query.add_filter('id','=',session['id']).fetch())
    if request.method == 'GET':
       
        query_post = datastore_client.query(kind='post')
       # query_post.order['-date_created']
        posts = list(query_post.fetch(limit=10))
        
        
        return render_template('forum.html', posts=posts, user=current_user[0])
        
    else:
        subject = request.form['subject']
        message = request.form['message']
        image = request.files['filename']

        if image:
            blob = bucket.blob(image.filename)
            blob.upload_from_string(
                image.read(),
                content_type = image.content_type
            )
            
            image_url = blob.public_url
        entity = datastore.Entity(datastore_client.key('post'))
        entity.update(
                {
                    "Subject":subject,
                    "Message":message,
                    "Author": current_user[0]['id'],
                    "Date_created": datetime.datetime.utcnow(),
                    "image_url": image_url
                }
            )
        datastore_client.put(entity)


        return redirect('/forum')



@app.route('/user', methods=['GET','POST'])
def user():
     if request.method=='GET':
        
        
        query_post = datastore_client.query(kind='post')
       # query_post.order['-date_created']
        posts = list(query_post.add_filter('Author','=',session['id']).fetch())
        query = datastore_client.query(kind='user')
        user = list(query.add_filter('id','=',session['id']).fetch())

        return render_template('user.html',posts=posts,user_name=user[0]['user_name'])
     
     else:
        
        old_pwd = request.form['password1']
        new_pwd = request.form['password2']
        query = datastore_client.query(kind='user')
        pwd_exists = list(query.add_filter('id','=',session['id']).fetch())
        key = datastore_client.key('user',pwd_exists[0].key.id)
        user = datastore_client.get(key)
        print(user)
        if user['password']==old_pwd:
            user['password']=new_pwd
            datastore_client.put(user)
            session.pop('id',None)
            return redirect('/')
        else:
            return render_template('user.html', message=msg[2])
          
  
     return render_template('user.html')
@app.route('/edit/<int:postid>')
def edit(postid):
    key = datastore_client.key('post',postid)
    post=datastore_client.get(key)
    if request.method=='GET':
        return render_template('edit.html',post=post)
    else:
        subject = request.form['subject']
        message = request.form['message']
        image = request.files['filename']

        if image:
            blob = bucket.blob(image.filename)
            blob.upload_from_string(
                image.read(),
                content_type = image.content_type
            )
            
            image_url = blob.public_url
            post['image_url']=image_url
        post['Subject']=subject
        post['Message']=message
        post_created = datetime.datetime.utcnow()
        datastore_client.put(post)
        return refirect('/forum')
    print(post)
    
@app.route('/logout')
def logout():
    session.pop('id', none)
    return redirect('/')

if __name__ == "__main__":
    app.run(host='localhost',debug=True)

