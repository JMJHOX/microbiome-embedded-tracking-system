import cv2
import requests
import datetime


def f(samples, img):
    print("info:", samples)
    if (len(samples) >= 5):
        requests.post('http://192.168.0.20/api/micro/createRegistry', data={
            "username": "joserapiw",
            "image": img,
            "sample_qty": len(faces)
        })


# We load the training data for our ML model
face_cascade = cv2.CascadeClassifier('data_trained.xml')

cap = cv2.VideoCapture(0)
# Look to what to do with our microbit

i = 0
start = datetime.datetime.now()
last = start
# start calling f now and every 60 sec thereafter
while True:

    # Read the frame
    _, img = cap.read()
    print(_)
    # Convert to grayscale(important to openCV, it can only identify on grayscale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    print("bip")
    # Display the image on our desktop
    cv2.imshow('img', img)
    now = datetime.datetime.now()
    if now - last > datetime.timedelta(seconds=10):
        #    retval, buffer = cv2.imencode('.jpg', img)
        #    jpg_as_text = base64.b64encode(buffer)
        #    print(jpg_as_text)
        f(faces)
        last = now
        print('Elapsed: ' + str(now-start) + ' | Iteration #')
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
# Release the VideoCapture object
cap.release()
