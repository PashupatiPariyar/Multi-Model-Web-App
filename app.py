import pickle
import numpy as np

from flask import Flask, request, render_template
from sklearn.feature_extraction.text import CountVectorizer

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


if __name__ == "__main__":
				app.run()