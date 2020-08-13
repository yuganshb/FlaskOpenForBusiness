import base64

from flask import Flask, render_template, request, Response, make_response

from video_camera import VideoCamera
import requests as rq
app = Flask(__name__)

video_stream = VideoCamera(0)
@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/distance_prediction')
def distance_prediction():

    return render_template('distance_prediction.html')


@app.route('/generateUUID', methods=['POST'])
def generate_uuid():
    form = request.form
    import uuid
    id = uuid.uuid1()
    with open('UserUniqueCode.csv', 'w') as f:
        f.write(str(form['Aadhar']) + ',' + form['MobileNumber'] + ',' + form['Name'] + ',' + str(id.int))
    print(str(id.int))
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + str(id.int)
    response = rq.get(qr_url)
    #with open('./static/img/sample.png', 'wb') as f:
        #f.write(response.content)
    b64_src = "data:image/jpeg;charset=utf-8;base64,"


    return render_template('qr.html', img_src = b64_src + base64.b64encode(response.content).decode('utf-8'))


@app.route('/maskDetection')
def show_webcam():
    return render_template('video_feed.html')


@app.route('/upload', methods=["POST"])
def transform_view():
    request_file = request.files['data_file']
    if not request_file:
        return "No file"

    #request_file.filename
    file_contents = request_file.stream.read()

    result = (file_contents)

    with open('result.mp4', 'wb') as f:
        f.write(result)


    return render_template('upload.html')

@app.route('/submit', methods=['POST'])
def submit():
    image = request.args.get('image')

    print(type(image))
    return ""


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    src = request.args.get('src')
    video_stream = VideoCamera(src)
    return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()
