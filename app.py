from flask import Flask,url_for, request,render_template,redirect, session
import os
from werkzeug.utils import secure_filename
import settings
import hashlib,binascii
from datetime import datetime
import urllib.request
import uploadflie
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
app.config.from_pyfile('settings.py')
#数据库对象
db = SQLAlchemy(app)


mydict = {
    'filename': '',
    'filemd5': '',
    'filetime': '',
    'filesize': '',
}



def getmd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__) 
        upload_path = os.path.join(basepath, 'upload_file_dir',secure_filename(f.filename))  
        f.save(upload_path)

        mydict['filename'] = secure_filename(f.filename)
        mydict['filemd5'] = getmd5(upload_path)
        mydict['filetime'] = datetime.now()
        filesize = os.path.getsize(upload_path)
        #保留两位小数
        mydict['filesize'] = ("%.2f" % (filesize/float(1024 * 1024)))

        mylist =[]
        mylist = uploadflie.uploadFile(mydict['filename'], upload_path)

        myjson = {
            'mydict' : mydict,
            'mylist' : mylist
        }
        session['myjson'] = myjson
        return render_template('upload.html')

    return render_template('index.html')

@app.route('/getSession',methods=['POST'])
def getSession():
    return session.get("myjson")

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  
        upload_path = os.path.join(basepath, 'upload_file_dir',secure_filename(f.filename))  
        f.save(upload_path)

        mydict['filename'] = secure_filename(f.filename)
        mydict['filemd5'] = getmd5(upload_path)
        mydict['filetime'] = datetime.now()
        filesize = os.path.getsize(upload_path)
        #保留两位小数
        mydict['filesize'] = ("%.2f" % (filesize/float(1024 * 1024)))

        mylist =[]
        mylist = uploadflie.uploadFile(mydict['filename'], upload_path)

        myjson = {
            'mydict' : mydict,
            'mylist' : mylist
        }
        session['myjson'] = myjson
        return render_template('upload.html', **mydict)
    return render_template('upload.html',  **mydict)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/private')
def private():
    return render_template('private.html')

@app.errorhandler(404)
def miss(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
