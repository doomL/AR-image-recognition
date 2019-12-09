from sys import stdout
import logging
from flask import Flask, render_template, Response, request, redirect,url_for
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
import numpy as np
from camera import Camera
#from Camera import Camera
from utils import base64_to_pil_image, pil_image_to_base64,stringToImage,findPoints
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

mysql=MySQL(app)


def switchAlg(number):
    if number == 0:
        return SurfAlgorithm()

    elif number == 1:
        return SiftAlgorithm()

    elif number == 2:
        return OrbAlgorithm()

# 0 = DEFAULT ALGORITHM SURF


currAlgorithm = 0 
algChoose = switchAlg(None)
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
    print(request.form["azienda"])
    cur = mysql.connection.cursor()
    
    #print(cur.execute("SELECT "))
    
    print(cur.execute("INSERT INTO user(username,password,email,azienda) VALUES(%s,%s,%s,%s,%s)" ,(request.form["name"] , request.form["pass"] , request.form["email"] , request.form["azienda"])))
    
    mysql.connection.commit()
    cur.close()

    return "OK"

@app.route('/login')
def login():
    return render_template('login.html')
     
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


@app.route("/sift/", methods=['GET','POST'])
def siftAlg():
    print("Sift servlet")
    # if context == None:
    #     print("Context prima A None")
    algChoose = switchAlg(1)
    context.setStrategy2(algChoose)
    camera = Camera(context)

    if context == None:
        print("Context dopo None")
    return render_template("Index.html")


@app.route("/surf/", methods=['GET','POST'])
def surfAlg():
    print("Surf servlet")
    # if context == None:
    #     print("Context prima A None")
    algChoose = switchAlg(0)
    context.setStrategy2(algChoose)
    camera = Camera(context)

    if context == None:
        print("Context dopo A None")
    return render_template('index.html')


@app.route("/orb/", methods=['GET','POST'])
def orbAlg():
    print("Orb servlet")
    # if context == None:
    #     print("Context prima A None")
    algChoose = switchAlg(2)
    context.setStrategy2(algChoose)
    camera = Camera(context)

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
    return render_template('admin.html')
    

@app.route('/landing',methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')
    
@app.route('/adminm',methods=['POST'])
def adminm():
    imgString=request.form["images[0][url]"].split(",")#[23:]
    cur = mysql.connection.cursor()
    print(cur.execute("INSERT INTO images(name,model,type,floor,base64) VALUES(%s,%s,%s,%s,%s)" ,(request.form["name"] , request.form["model"] , request.form["type"] , request.form["floor"] , imgString[1])))
    mysql.connection.commit()
    cur.close()
    findPoints(imgString[1])
    return render_template('init.html')


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5000)
    



