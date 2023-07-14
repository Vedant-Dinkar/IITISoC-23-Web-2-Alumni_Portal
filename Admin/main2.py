from flask import Flask,render_template,request,url_for,redirect
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import gridfs
from email.message import EmailMessage
import ssl
import smtplib
from datetime import date









app = Flask(__name__)

client = MongoClient('localhost', 27017)
app.config['MONGO_URI']='mongodb://localhost:27017'
mongo=PyMongo(app)
db = client.Alumni_Admin
EVENTS = db.Events
MAILS=db.Mails
fs=gridfs.GridFS(db)



@app.route('/')
def hello():
    return render_template('home.html')


#---------------------------EVENTS---------------------------------

@app.route('/eventsext', methods=('GET', 'POST'))
def eventsext():
    if request.method=='POST':
        event_name = request.form['event_name']
        schedule = request.form['schedule']
        description = request.form['description']
        EVENTS.insert_one({'event_name': event_name, 'schedule': schedule, 'description':description})
        return redirect(url_for('events'))
    return render_template('eventsext.html')

@app.post('/events/<id>/delete/')
def delete(id):
    # eventtobedeleted={'_id':ObjectId(id)}
    EVENTS.delete_one({"_id":ObjectId(id)})
    # events.delete_one(eventtobedeleted)
    return redirect(url_for('events'))


@app.route('/events')
def events():
    all_events = EVENTS.find()
    return render_template('events.html', events=all_events)







# --------------------------------------GALLERY--------------

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
    images=fs.find()
    return render_template('gallery.html', images=images)


@app.route('/auth')
def auth():
    return render_template('layout.html')







# --------------------------MAILS----------------------------------------
@app.route('/mail')
def mail():
    all_mails=MAILS.find()
    return render_template('mail.html',mails=all_mails)

@app.route('/mailsext', methods=['GET','POST'])
def mailsext():
    email_sender='cse220001020@iiti.ac.in'
    email_password='cbkdnqyakmtiekdh'   
    if request.method=='POST':
        email_receiver=request.form['email']
        subject=request.form['subject']
        body=request.form['message']
        today=date.today()
        today_string = today.strftime("%Y-%m-%d")


        MAILS.insert_one({'to': email_receiver, 'subject': subject, 'body':body,'date':today_string})

        em=EmailMessage()
        em['From']=email_sender
        em['To']=email_receiver
        em['Subject']=subject
        em.set_content(body)

        context=ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())
        return redirect(url_for('mail'))
    return render_template('mailsext.html')









# --------------------------------FORUMS------------------------
@app.route('/forums')
def forums():
    return render_template('forums.html')





if __name__=="__main__":
    app.run(debug=True)