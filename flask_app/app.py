from sys import stdout
import logging
from flask import Flask, render_template, Response, request, redirect,url_for, abort,jsonify,session,json
from flask_socketio import SocketIO,send,emit
from flask_mysqldb import MySQL
import numpy as np
from camera import Camera
#from Camera import Camera
from utils import base64_to_pil_image, pil_image_to_base64,stringToImage,findPoints,loadImg,toRGB
import cv2
import AlgorithmChooser
from AlgorithmChooser import SiftAlgorithm,SurfAlgorithm,OrbAlgorithm,AkazeAlgorithm,OrbHarrisAlgorithm
from Context import Context
from flask_sqlalchemy import SQLAlchemy
from Database import Database
from uuid import UUID
import cv2
# from database import User,Images,Azienda


app = Flask(__name__)
#app.logger.addHandler(logging.StreamHandler(stdout))
log= logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:''@localhost/arsistant'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'':''@localhost/alchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# CREO IL SOCKET
socketio = SocketIO(app)

#Database Configuration
database = Database(app)

# loadToDb = False
# CREO GLI OGGETTI DEL DB

class User(database.db.Model):

    username = database.db.Column(database.db.String(30),primary_key=True)
    password = database.db.Column(database.db.String(30))
    azienda = database.db.Column(database.db.String(20))
    email = database.db.Column(database.db.String(30),unique = True)
    admin = database.db.Column(database.db.Boolean)

    def __init__(self,username,password,azienda,email,admin):
        self.username = username
        self.password = password
        self.azienda = azienda
        self.email = email
        self.admin = admin

class Imagesdata(database.db.Model):
    id = database.db.Column(database.db.Integer,primary_key=True)
    idimg = database.db.Column(database.db.Integer)
    harrisDescriptor= database.db.Column(database.db.String(64))
    harrisKeypoints= database.db.Column(database.db.String(4294000000))

    def __init__(self,idimg,harrisDescriptor,harrisKeypoints):
        self.idimg=idimg
        self.harrisDescriptor = harrisDescriptor
        self.harrisKeypoints = harrisKeypoints


class Images(database.db.Model):

    id = database.db.Column(database.db.Integer,primary_key=True)
    name = database.db.Column(database.db.String(30))
    model = database.db.Column(database.db.String(20))
    type = database.db.Column(database.db.String(20))
    floor = database.db.Column(database.db.String(20))
    azienda = database.db.Column(database.db.String(20))
    # path = database.db.Column(database.db.String(20))
    base64 = database.db.Column(database.db.String(4294000000))
    
    

    def __init__(self,name,model,type,floor,base64,azienda):
        self.name = name
        self.model = model
        self.type = type
        self.floor = floor
        self.base64 = base64
        self.azienda = azienda

    
class Azienda(database.db.Model):

    id = database.db.Column(database.db.Integer,primary_key=True)
    name = database.db.Column(database.db.String(30))
    code = database.db.Column(database.db.String(30))
    floors = database.db.Column(database.db.String(2))

    def __init__(self,name):
        self.name = name

# popolo il db con le tabelle vuote
# database.db.create_all() 

# username password azienda mail admin
# ines = User("Inessina", "ciao","chimica","ines@gmail.com",False)
#aggiungo così
# database.db.session.add(ines)
# database.db.session.commit()

# per vedere se esiste qualcosa con quell'attributo
# esiste = database.db.session.query(User).filter_by(username='tappeto').first()
# print("esiste : ",esiste)
# si elimina così
# database.db.session.delete(User.query.filter_by(username='Inessina').first())
# database.db.session.commit()

# database.db.session.add(Imagesdata(1,"a","a"))
# database.db.session.commit()

def switchAlg(number,loader):
    if number == 0:
        return SurfAlgorithm(loader)

    elif number == 1:
        return SiftAlgorithm(loader)

    elif number == 2:
        return OrbAlgorithm(loader)

    elif number == 3:
        return AkazeAlgorithm(loader)

    elif number == 4:
        return OrbHarrisAlgorithm(loader)

        

# 0 = DEFAULT ALGORITHM SURF


currAlgorithm = 0 
algChoose = switchAlg(None,None)
context = Context(algChoose)
camera = Camera(context)
# surfAlg()


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")

@socketio.on('input image', namespace='/test')
def test_message(input):
    # print(input)
    input = input.split(",")[1]
    # print("ENTRO QUAAAAAAAAAAAAA")
    camera.enqueue_input(input)
    #camera.enqueue_input(base64_to_pil_image(input))
    if camera.get_result()!=None:       
        # recObj = database.db.session.query(Images).filter_by(id=).first()
        emit('responseImageInfo',getObject(camera.get_result()))
    # socketio.send(13421)

# DA MODIFICAREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
@app.route('/getObject',methods=['POST','GET']) 
def getObject(curr_id):
    recognizedObject = database.db.session.query(Images).filter_by(id=curr_id).first()

    obj = {
        'id': recognizedObject.id,
        'name': recognizedObject.name,
        'model':recognizedObject.model,
        'type':recognizedObject.type,
        'floor':recognizedObject.floor,
        'base64':recognizedObject.base64

    }
    # print(obj)
    return json.dumps(obj)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('landing.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

# DA MODIFICARE FORSE INUTILIZZATA, registrazione vecchia
# @app.route('/registration', methods=['POST'])
# def registration():

#     cur = mysql.connection.cursor()
    
#     #Trovare azieda con codiceAzienda
#     selectQuery="SELECT * FROM azienda WHERE code = %s" 
    
#     if not cur.execute(selectQuery,(request.form["azienda"],)):
#         return jsonify(message='AziendaCode_error'),500


#     print(cur.execute("INSERT INTO user(username,password,email,azienda,admin) VALUES(%s,%s,%s,%s,%s)" ,(request.form["name"] , request.form["pass"] , request.form["email"] , request.form["azienda"],0)))
    
#     mysql.connection.commit()
#     cur.close()

#     return "OK"



@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login1', methods=['POST'])
def accedi():

    esisteUtente = database.db.session.query(User).filter_by(password=request.form["pass"],username = request.form["name"]).first()

    if esisteUtente != None:
        session["username"]=request.form["name"]
        session["loggato"]=1
        azienda = database.db.session.query(User.azienda).filter_by(username = request.form["name"]).first()
        session["azienda"]=azienda
        # print(session["azienda"])
        isAdmin = database.db.session.query(User).filter_by(username = request.form["name"],admin=1).first()
        # print("is admin : ",isAdmin)
        if isAdmin != None:
            session["admin"] = 1
        # print("PUOI ACCEDERE")
        return "ACCESSO EFFETTUATO"

    
    return jsonify(message='Username O Password Errati'),500



@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username',None)
    session.pop('azienda',None)
    session.pop('admin',None)
    session["loggato"]=0
    # session.clear()
    return render_template('landing.html')


@app.route("/saveVideo/", methods=['POST'])
def saveVideo():
    if int(request.form['json_str'])%2==0:
        # print("Servlet di save video") 
        camera.recording(True)
    elif int(request.form['json_str'])%2!=0:
        # print("Servlet di stop video")
        camera.stopRec(False)    
    return "OK"


@app.route("/surf/", methods=['GET','POST'])
def surfAlg():
    print("Surf servlet")
    # if context == None:
    #     print("Context prima A None")
    # loader=loadImg(mysql,session)
    loader=loadImg(database.db,session,Images)
    algChoose = switchAlg(0,loader) #1
    context.setStrategy2(algChoose)
    camera = Camera(context)
    session["algorithm"]=1 #

    # if context == None:
    #     # print("Context dopo A None")
    return render_template('index.html')



@app.route("/akaze/", methods=['GET','POST'])
def akazeAlg():
    print("Akaze servlet")
    # if context == None:
    #     print("Context prima A None")
    # loader=loadImg(mysql,session)
    loader=loadImg(database.db,session,Images)
    algChoose = switchAlg(3,loader)
    context.setStrategy2(algChoose)
    camera = Camera(context)
    session["algorithm"]=4

    # if context == None:
    #     print("Context dopo A None")
    return render_template('index.html')



@app.route("/sift/", methods=['GET','POST'])
def siftAlg():
    print("Sift servlet")
    # if context == None:
    #     print("Context prima A None")
    # loader=loadImg(mysql,session)
    loader=loadImg(database.db,session,Images)
    algChoose = switchAlg(1,loader)
    context.setStrategy2(algChoose)
    camera = Camera(context)
    session["algorithm"]=2

    # if context == None:
    #     print("Context dopo None")
    return render_template("Index.html")


@app.route("/orb/", methods=['GET','POST'])
def orbAlg():
    print("Orb servlet")
    # if context == None:
    #     print("Context prima A None")
    # loader=loadImg(mysql,session)
    loader=loadImg(database.db,session,Images)
    algChoose = switchAlg(2,loader)
    context.setStrategy2(algChoose)
    camera = Camera(context)
    session["algorithm"]=3

    # if context == None:
    #     print("Context dopo None")
    return render_template("Index.html")


@app.route("/orbHarris/", methods=['GET','POST'])
def orbHarrisAlg():
    print("OrbHarris servlet")
    # if context == None:
    #     print("Context prima A None")
    # loader=loadImg(mysql,session)
    loader=loadImg(database.db,session,Images)
    algChoose = switchAlg(4,loader) 
    context.setStrategy2(algChoose)
    camera = Camera(context)
    session["algorithm"]=5 

    # if context == None:
    #     print("Context dopo A None")
    return render_template('index.html')

def gen():
    """Video streaming generator function."""

    app.logger.info("starting to generate frames!")
    # cv2.imwrite("frame3.png",camera.get_frame())
    while True:
        # print("++++++++++++++++")
        frame = camera.get_frame() #pil_image_to_base64(camera.get_frame())
        # print("*************")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/information')
def sendInformation():
    pass



@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # print ("VIDEO FEED")
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/admin',methods=['GET', 'POST'])
def mostraImmaginiManager():

    aziendaImg = database.db.session.query(Images).filter_by(azienda=session["azienda"]).all()

    return render_template('admin.html', images=aziendaImg)



# ADMIN CHE PUO AGGIUNGERE UTENTI, SOLO SE NON GIA REGISTRATI NE CON LA MAIL NE CON LO USERNAME
@app.route('/addUser',methods=['GET', 'POST'])
def addUser():

    esisteUsername = database.db.session.query(User).filter_by(username=request.form["username"]).first()
    esisteMail = database.db.session.query(User).filter_by(email=request.form["email"]).first()

    # print("Esiste username",esisteUsername)
    # print("Esiste mail",esisteMail)

    # aggiungo solo se non ho ne lo username e ne la mail nel db
    if esisteUsername == None and esisteMail == None:

        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        azienda = session["azienda"]


        nuovoUtente = User(username, password,azienda,email,False)
        database.db.session.add(nuovoUtente)
        database.db.session.commit()
        print("AGGIUNGO NUOVO UTENTE")
    else:
        print("NON AGGIUNGO UTENTE GIA REGISTRATO")


    return render_template('landing.html')


@app.route('/deleteUser',methods=['GET', 'POST'])
def deleteUser():

    esisteUsername = database.db.session.query(User).filter_by(username=request.form["usernameDaEliminare"]).first()
    # esisteMail = database.db.session.query(User).filter_by(email=request.form["emailDaEliminare"]).first()

    print("Esiste username",esisteUsername)
    # print("Esiste mail",esisteMail)

    # inserisco lo username da cancellare, se c'e' elimino
    if not esisteUsername == None:
        database.db.session.delete(User.query.filter_by(username=request.form["usernameDaEliminare"]).first())
        database.db.session.commit()
        # print("ELIMINATO")
        return "ELIMINATO"

    # print("NON ELIMINATO")
    return "NON ELIMINATO"



# funziona
@app.route('/deleteImg',methods=['POST'])
def deleteImg():
    
    # print("ID E' : ",request.form['id'])

    database.db.session.delete(Images.query.filter_by(id=request.form['id']).first())
    database.db.session.commit()

    return "OK deleteImg"

    
    

@app.route('/landing',methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')
    
@app.route('/adminm',methods=['POST'])
def aggiungiImmagine():

    imgString=request.form["images[0][url]"].split(",")#[23:]
    nuovaImmagine = Images(request.form["name"] , request.form["model"] , request.form["type"] , request.form["floor"] , imgString[1],session["azienda"])
    database.db.session.add(nuovaImmagine)
    database.db.session.commit()
    # database.db.session.flush()
    # idImg = database.db.session.query(Images.id).filter_by(name=request.form['id']).first())
    # calcolaDatiImg(nuovaImmagine.id,imgString[1])
    print("immagine aggiunta")
    return "OK"


def calcolaDatiImg(idImg,base64):
    detector = cv2.ORB_create(nfeatures=500)
    img = toRGB(stringToImage(base64))
    keyP = detector.detectAndCompute(img,None)[0]
    desc = detector.detectAndCompute(img,None)[1]
    print("ID IMG ", idImg)
    print("ID KEY ", keyP)
    print("ID DESC ", desc)
    nuoviDati = Imagesdata(idImg,"desc",keyP)

    database.db.session.add(nuoviDati)
    database.db.session.commit()
    




if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5000)
    



