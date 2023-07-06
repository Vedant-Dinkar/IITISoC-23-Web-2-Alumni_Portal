from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/events')
def events():
    return render_template('events.html')

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

@app.route('/galleryext')
def galleryext():
    return render_template('galleryext.html')

if __name__=="__main__":
    app.run(debug=True)