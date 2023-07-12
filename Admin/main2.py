from flask import Flask,render_template,request,url_for,redirect
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import gridfs
import os


app = Flask(__name__)

client = MongoClient('localhost', 27017)
app.config['MONGO_URI']='mongodb://localhost:27017'
mongo=PyMongo(app)
db = client.Alumni_Admin
EVENTS = db.Events
# GALLERY=db.event_gallery
fs=gridfs.GridFS(db)



@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/eventsext', methods=('GET', 'POST'))
def eventsext():
    if request.method=='POST':
        event_name = request.form['event_name']
        schedule = request.form['schedule']
        description = request.form['description']
        EVENTS.insert_one({'event_name': event_name, 'schedule': schedule, 'description':description})
        return redirect(url_for('events'))
    return render_template('eventsext.html')

# @app.post('/<id>/delete/')
# def delete(id):
#     events.delete_one({"_id": ObjectId(id)})
#     return redirect(url_for('events'))


@app.route('/events')
def events():
    all_events = EVENTS.find()
    return render_template('events.html', events=all_events)





@app.route('/galleryext', methods=('GET', 'POST'))
def gallerysext():
    if request.method=='POST':
        event_gallery_name = request.form['event_gallery_name']
        image_file = request.files['gallery_image']
        file_data=image_file.read()
        fs.put(file_data,filename=event_gallery_name)
        return redirect(url_for('gallery'))
    return render_template('galleryext.html')

# @app.route('/gallery')
# def gallery():
#     all_pics = mongo.db.Alumni_Admin.find()
#     return render_template('gallery.html', pics=all_pics)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/auth')
def auth():
    return render_template('layout.html')

@app.route('/mail')
def mail():
    return render_template('mail.html')


@app.route('/forums')
def forums():
    return render_template('forums.html')

@app.route('/mailsext')
def mailsext():
    return render_template('mailsext.html')




if __name__=="__main__":
    app.run(debug=True)