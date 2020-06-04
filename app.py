from flask import Flask, request, jsonify, render_template
import pickle


app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/height_weight', methods=['GET', 'POST'])
def predict_weight():

	global weights

	if request.method == 'POST':
		height = float(request.form['height'])
		gender = float(request.form['gender'])

		prediction = model.predict([[gender, height]])

		weights = round(prediction[0], 2)

		return render_template('height_weight.html', weights='Your Weight is: {}'.format(weights))

		if __name__ == "__main__":
			app.run()
