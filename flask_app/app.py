from sys import stdout
import logging
from flask import Flask, render_template, Response, request, redirect
from flask_socketio import SocketIO
from camera import Camera
from utils import base64_to_pil_image, pil_image_to_base64
import cv2
import AlgorithmChooser
from AlgorithmChooser import SiftAlgorithm,SurfAlgorithm
from Context import Context


app = Flask(__name__)
#app.logger.addHandler(logging.StreamHandler(stdout))
log= logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)



def switchAlg(number):
    if number == 0:
        return SurfAlgorithm()
    elif number == 1:
        return SiftAlgorithm()

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
    return render_template('init.html')


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
    print("Servlet di save video, per ora non va")
    #camera.__del__()


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


@app.route("/sift/", methods=['POST'])
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


@app.route("/surf/", methods=['POST'])
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


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5000)
    



