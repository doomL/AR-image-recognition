from sys import stdout
import logging
from flask import Flask, render_template, Response, request, redirect,url_for, abort,jsonify,session
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
import numpy as npMySQL
from camera import Camera
#from Camera import Camera
from utils import base64_to_pil_image, pil_image_to_base64,stringToImage,findPoints,loadImg
import cv2
import AlgorithmChooser
from AlgorithmChooser import SiftAlgorithm,SurfAlgorithm,OrbAlgorithm
from Context import Context

app = Flask(__name__)
#app.logger.addHandler(logging.StreamHandler(stdout))
log= logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)

#Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_DB'] = 'arsistant'

# app.config['MYSQL_HOST'] = '192.168.1.145'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_DB'] = 'arsistant'
# app.config['MYSQL_PORT'] = '3306'

mysql=MySQL(app)
  

def switchAlg(number,loader):
    if number == 0:
        return SurfAlgorithm(loader)

    elif number == 1:
        return SiftAlgorithm(loader)

    elif number == 2:
        return OrbAlgorithm(loader)

# 0 = DEFAULT ALGORITHM SURF


currAlgorithm = 0 
algChoose = switchAlg(None,None)
context = Context(algChoose)
camera = Camera(context)
# surfAlg()

@socketio.on('input image', namespace='/test')
def test_message(input):
    input = input.split(",")[1]
    camera.enqueue_input(input)
    #camera.enqueue_input(base64_to_pil_image(input))


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('landing.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/registration', methods=['POST'])
def registration():
    cur = mysql.connection.cursor()
    
    #Trovare azieda con codiceAzienda
    selectQuery="SELECT * FROM azienda WHERE code = %s" 
    
    if not cur.execute(selectQuery,(request.form["azienda"],)):
        return jsonify(message='AziendaCode_error'),500


    print(cur.execute("INSERT INTO user(username,password,email,azienda,admin) VALUES(%s,%s,%s,%s,%s)" ,(request.form["name"] , request.form["pass"] , request.form["email"] , request.form["azienda"],0)))
    
    mysql.connection.commit()
    cur.close()

    return "OK"
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login1', methods=['POST'])
def login1():
    username=request.form["name"]
    password=request.form["pass"]
    cur = mysql.connection.cursor()

    selectQuery="SELECT * FROM user WHERE username = %s AND password = %s" 

    aziendaQuery="SELECT azienda FROM user WHERE username = %s "
    
    adminQuery="SELECT * FROM user WHERE username = %s AND admin = 1"
    if cur.execute(selectQuery,(username,password)):
        session["username"]=username
        cur.execute(aziendaQuery,(username,))
        aziende=cur.fetchone()
        azienda=aziende[0]

        isAdmin=cur.execute(adminQuery,(username,))                          
        print(isAdmin)
        mysql.connection.commit()
        cur.close()
        session["azienda"]=azienda
        session["admin"]=isAdmin
        session["loggato"]=1
        print("CHEéEéEéEéEéEEéEéEéE")
        return "OK"
    else:
        return jsonify(message='Username O Password Errati'),500


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username',None)
    session.pop('azienda',None)
    session.pop('admin',None)
    session["loggato"]=0
    # session.clear()
    return render_template('landing.html')

     
# @app.route("/chooseAlg", methods=['POST'])
# def chooseAlg():
#     print("CambioAlgoritmo")
#     currAlgorithm=request.form.get("alg")
#     print(currAlgorithm)
#     context = Context.Context(switchAlg(currAlgorithm))
#     camera = Camera(context)
#     return render_template("index.html")



@app.route("/saveVideo/", methods=['POST'])
def saveVideo():
    if int(request.form['json_str'])%2==0:
        print("Servlet di save video") 
        camera.recording(True)
    elif int(request.form['json_str'])%2!=0:
        print("Servlet di stop video")
        camera.stopRec(False)    
    return "OK"

# @app.route("/surf/", methods=['POST'])
# def surfAlg():
#     print("Surf servlet")
#     # if context == None:
#     #     print("Context prima A None")
#     algChoose = switchAlg(0)
#     context=Context.setStrategy2(algChoose)
#     camera = Camera(context)
#     if context == None:
#         print("Context dopo A None")
#     return render_template("index.html")

@app.route("/surf/", methods=['GET','POST'])
def surfAlg():
    print("Surf servlet")
    # if context == None:
    #     print("Context prima A None")
    loader=loadImg(mysql,session)
    algChoose = switchAlg(0,loader)
    context.setStrategy2(algChoose)
    camera = Camera(context)
    session["algorithm"]=1

    if context == None:
        print("Context dopo A None")
    return render_template('index.html')

@app.route("/sift/", methods=['GET','POST'])
def siftAlg():
    print("Sift servlet")
    # if context == None:
    #     print("Context prima A None")
    loader=loadImg(mysql,session)
    algChoose = switchAlg(1,loader)
    context.setStrategy2(algChoose)
    camera = Camera(context)
    session["algorithm"]=2

    if context == None:
        print("Context dopo None")
    return render_template("Index.html")




@app.route("/orb/", methods=['GET','POST'])
def orbAlg():
    print("Orb servlet")
    # if context == None:
    #     print("Context prima A None")
    loader=loadImg(mysql,session)
    algChoose = switchAlg(2,loader)
    context.setStrategy2(algChoose)
    camera = Camera(context)
    session["algorithm"]=3

    if context == None:
        print("Context dopo None")
    return render_template("Index.html")

def gen():
    """Video streaming generator function."""

    app.logger.info("starting to generate frames!")
    while True:
        frame = camera.get_frame() #pil_image_to_base64(camera.get_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    print ("prunt")
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/admin',methods=['GET', 'POST'])
def admin():
    selectImageQuery="SELECT * FROM images WHERE azienda = %s" 
        
    cur = mysql.connection.cursor()
        
    cur.execute(selectImageQuery,(session["azienda"],))

    dbImages=cur.fetchall()

    return render_template('admin.html', images=dbImages)
    

@app.route('/deleteImg',methods=['POST'])
def deleteImg():
    cur = mysql.connection.cursor()
    print(request.form['id'])
    deleteQuery="DELETE FROM images WHERE id = %s "
    cur.execute(deleteQuery,(request.form["id"],))

    mysql.connection.commit()

    cur.close()

    return "OK deleteImg"

    
    

@app.route('/landing',methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')
    
@app.route('/adminm',methods=['POST'])
def adminm():
    imgString=request.form["images[0][url]"].split(",")#[23:]
    cur = mysql.connection.cursor()
    print(cur.execute("INSERT INTO images(name,model,type,floor,base64,azienda) VALUES(%s,%s,%s,%s,%s,%s)" ,(request.form["name"] , request.form["model"] , request.form["type"] , request.form["floor"] , imgString[1],session["azienda"])))
    mysql.connection.commit()
    cur.close()
    findPoints(imgString[1])
    return render_template('init.html')


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5000)
    



