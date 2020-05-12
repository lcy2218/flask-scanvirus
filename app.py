from flask import Flask,url_for, request,render_template,redirect, session
import os
from werkzeug.utils import secure_filename
import settings
import hashlib,binascii
from datetime import datetime
import urllib.request
import uploadflie
from flask_sqlalchemy import SQLAlchemy
import checkpe
app = Flask(__name__)
app.secret_key = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
app.config.from_pyfile('settings.py')

#数据库操作
db = SQLAlchemy(app)
#数据库模型
class User_info(db.Model):
    __tablebname__ = "user_info"
    id = db.Column(db.Integer, primary_key = True)
    u_ip = db.Column(db.String(20))
    u_md5 = db.Column(db.String(50))
    u_count = db.Column(db.Integer)
    u_date = db.Column(db.Date)

    def __init__(self, u_ip, u_md5, u_count, u_date):
        self.u_ip = u_ip
        self.u_md5 = u_md5
        self.u_count = u_count
        self.u_date = u_date


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
        user_ip = request.remote_addr
        filesize = os.path.getsize(upload_path)
        #保留两位小数
        mydict['filesize'] = ("%.2f" % (filesize/float(1024 * 1024)))
        #用于存储上传结果
        mylist =[]
        #上传扫描
        mylist = uploadflie.uploadFile(mydict['filename'], upload_path)
        #存储机器学习结果
        mycheck = {}
        #机器学习扫描
        ispe = 0
        if os.path.splitext(upload_path)[1] == '.exe' or os.path.splitext(upload_path)[1] == '.dll' or os.path.splitext(upload_path)[1] == '.sys' or os.path.splitext(upload_path)[1] == '.ocx':
            mycheck = checkpe.output_result(upload_path)
            ispe = 1
        myjson = {
            'mydict' : mydict,
            'mylist' : mylist,
            'mycheck' : mycheck,
            'session_flag' : 0,
            'ispe': ispe
        }
        session['myjson'] = myjson

        session_flag = 0
        #数据库操作
        count = User_info.query.filter(User_info.u_ip==user_ip).count()
        count += 1
        if count > 10:
            myjson['session_flag'] = 1
            #返回给ajax的success   可以使用string, dict, tuple, Response instance, or WSGI callable
            return myjson
        else:
            user_info = User_info(user_ip, mydict['filemd5'], count, mydict['filetime'])
            db.session.add(user_info)
            db.session.commit()
            return myjson

    return render_template('index.html')

@app.route('/outcount')
def outcount():
    return render_template('outcount.html')

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
        user_ip = request.remote_addr
        filesize = os.path.getsize(upload_path)
        #保留两位小数
        mydict['filesize'] = ("%.2f" % (filesize/float(1024 * 1024)))

        mylist =[]
        #上传扫描
        mylist = uploadflie.uploadFile(mydict['filename'], upload_path)
        #存储机器学习结果
        mycheck = {}
        #机器学习扫描
        ispe = 0
        if os.path.splitext(upload_path)[1] == '.exe' or os.path.splitext(upload_path)[1] == '.dll' or os.path.splitext(upload_path)[1] == '.sys' or os.path.splitext(upload_path)[1] == '.ocx' :
            mycheck = checkpe.output_result(upload_path)
            ispe = 1
        myjson = {
            'mydict' : mydict,
            'mylist' : mylist,
            'mycheck' : mycheck,
            'session_flag' : 0,
            'ispe': ispe
        }
        session['myjson'] = myjson

        session_flag = 0
        #数据库操作
        count = User_info.query.filter(User_info.u_ip==user_ip).count()
        count += 1
        if count > 10:
            myjson['session_flag'] = 1
            #返回给ajax的success   可以使用string, dict, tuple, Response instance, or WSGI callable
            return render_template('outcount.html')
        else:
            user_info = User_info(user_ip, mydict['filemd5'], count, mydict['filetime'])
            db.session.add(user_info)
            db.session.commit()
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
