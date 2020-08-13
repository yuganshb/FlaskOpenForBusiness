from flask import Flask, render_template, request, Response

from video_camera import VideoCamera

app = Flask(__name__)

video_stream = VideoCamera()
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


@app.route('/maskDetection')
def show_webcam():
    return render_template('video_feed.html')


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
    return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()
