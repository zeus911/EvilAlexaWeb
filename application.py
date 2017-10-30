from flask import Flask
from flask import render_template
from flask import request
import boto3


def sendToQueue(txt):
	sqs = boto3.resource('sqs', region_name='us-east-1')
	queue = sqs.Queue('https://sqs.us-east-1.amazonaws.com/192158051712/EvilAlexaQueue')
	response = queue.send_message(
		MessageBody=txt,
		)
	return response.get('MessageId')

application = Flask(__name__)
application.debug = True

@application.route('/', methods=['GET'])
def hello():
	return render_template('home.html')

@application.route('/speak', methods=['POST', 'GET'])
def login():
	user_message = ""
	txt = request.form['txt'].strip()
	txt = txt[:500]
	if (not txt):
		user_message = "No text entered!"
	else:
		messageId = sendToQueue(txt)
		user_message = "Thank you. Will say \"" + txt + "\" soon."
	return render_template('thankyou.html', user_message = user_message)

if __name__ == "__main__":
	application.run()



