from flask import Flask, render_template, Response
import cv2
import requests
import datetime
import numpy
app = Flask(__name__)

camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

# We load the training data for our ML model
face_cascade = cv2.CascadeClassifier('data_trained.xml')
i = 0
#start = datetime.datetime.now()
#last = start


def f(samples, img):

    print("info:", samples)
    if (len(samples) >= 2):
        stream = open("test.png", "rb")
        bytes = bytearray(stream.read())
        files = {'image': ('image.png', open('test.png', 'rb'),
                           'image/png', {'Expires': '0'})}
        photo_filename = requests.post(
            'http://192.168.0.20:3300/api/micro/upload',

            files=files
        )
        print(photo_filename.json()["filename"])

        x = requests.post(
            'http://192.168.0.20:3300/api/micro/createRegistry', data={
                "username": "joserapiw",
                "sample_qty": len(samples),
                'image_route_file':  photo_filename.json()["filename"],
            })

        print(x.text)


def gen_frames():  # generate frame by frame from camera
    start = datetime.datetime.now()
    last = start
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            x1 = x
            x2 = x + w
            y1 = y
            y2 = y + h
            if (len(faces) == 1):
                print("move X to ({}) AND Y to ({}) ".format(x, y))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # print("bip")
        # Display the image on our desktop
        #cv2.imshow('img', frame)
        cv2.imwrite("test.png", frame)
        now = datetime.datetime.now()
        if now - last > datetime.timedelta(seconds=10):
            #    retval, buffer = cv2.imencode('.jpg', img)
            #    jpg_as_text = base64.b64encode(buffer)
            #    print(jpg_as_text)
            f(faces, frame)

            last = now
    # Release the VideoCapture object
   # cap.release()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
