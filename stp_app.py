import base64
import io
from io import StringIO
import numpy as np
import cv2
import imutils
from PIL import Image
from flask import Flask, render_template, request
# Socket IO Dependencies
from flask_socketio import SocketIO, emit

from mask_detection.mask_detect import mask_detect

app = Flask(__name__)
# Initalizing SocketIO
socketio = SocketIO(app)


@app.route('/')
def hello():
    return render_template('home.html')



@app.route('/generateUUID', methods=['POST'])
def generate_uuid():
    form = request.form
    import uuid
    id = uuid.uuid1()
    with open('UserUniqueCode.csv', 'w') as f:
        f.write(str(form['Aadhar']) + ',' + form['MobileNumber'] + ',' + form['Name'] + ',' + str(id.int))
    print(str(id.int))

    return str(id.int)

@app.route('/mask_detect')
def home():
    print("SERVER STARTED")
    return render_template('index.html')


# Creating a SocketIO connetion named connect to initially test connection
@socketio.on('connect')
def test_connect():
    print("SOCKET CONNECTED")


@socketio.on('image', namespace='/mask_detect')
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    # Process the image frame
    frame = np.array(pimg)
    #frame = imutils.resize(pimg, width=700)
    frame = mask_detect(frame)
    print(frame);
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgencode = cv2.imencode('.jpeg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpeg;charset=utf-8;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)


if __name__ == '__main__':
    # Joining the socket to the App
    socketio.run(app)