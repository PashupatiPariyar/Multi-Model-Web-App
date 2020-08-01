import os
import cv2
import pickle
import numpy as np

from flask import Flask, request, render_template
from sklearn.feature_extraction.text import CountVectorizer
from keras.models import model_from_json
from keras.preprocessing import image
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
	return render_template('home.html')


@app.route('/height_weight', methods=['GET', 'POST'])
def predict_weight():
	model = pickle.load(open('model.pkl', 'rb'))
	if request.method == 'POST':
		height = float(request.form['height'])
		gender = float(request.form['gender'])
		prediction = model.predict([[gender, height]])

		weights = round(prediction[0], 2)

		return render_template('height_weight.html', weights='Your Weight is: {}'.format(weights))
	return render_template('height_weight.html')

@app.route('/spam_ham', methods=['GET', 'POST'])
def predict_message():
	model = pickle.load(open('spam_ham.pkl','rb')) 
	if request.method == 'POST':
		message = request.form['detect']

		data = [message]
		data =  np.array(data)

		prediction = model.predict(data)

		if prediction == 1:
			messages = "Spam"
		else:
			messages = "Ham" 

		if type(messages)==type('string'):
			return render_template('spam_ham.html', message='Your Message is: {}'.format(messages))
		else:
			return render_template('spam_ham.html', message='Your Message is: {}'.format(messages))
	return render_template('spam_ham.html')

@app.route('/face_emotion', methods=['GET', 'POST'])
def face_emotion():
    #load model
    model = model_from_json(open("fer.json", "r").read())
    #load weights
    model.load_weights('fer.h5')


    face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    cap=cv2.VideoCapture(0)

    while True:
        ret,test_img=cap.read()# captures frame and returns boolean value and captured image
        if not ret:
            continue
        gray_img= cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)

        faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)


        for (x,y,w,h) in faces_detected:
            cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=7)
            roi_gray=gray_img[y:y+w,x:x+h]#cropping region of interest i.e. face area from  image
            roi_gray=cv2.resize(roi_gray,(48,48))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis = 0)
            img_pixels /= 255

            predictions = model.predict(img_pixels)

            #find max indexed array
            max_index = np.argmax(predictions[0])

            emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
            predicted_emotion = emotions[max_index]

            cv2.putText(test_img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        resized_img = cv2.resize(test_img, (1000, 700))
        cv2.imshow('Facial emotion analysis ',resized_img)



        if cv2.waitKey(10) == ord('q'):#wait until 'q' key is pressed
            break

    cap.release()
    cv2.destroyAllWindows


if __name__ == "__main__":
				app.run()
