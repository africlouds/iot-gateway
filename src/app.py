from flask import Flask, request, flash, url_for, redirect, render_template
from flask.ext.jsonpify import jsonify
from flask_sqlalchemy import SQLAlchemy
import flask.ext.httpauth
from time import gmtime, strftime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///readings.sqlite3'
app.config['SECRET_KEY'] = "random string"
auth = flask.ext.httpauth.HTTPBasicAuth()
db = SQLAlchemy(app)

users = {
    "admin": "admin"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

class Reading(db.Model):
   id = db.Column('reading_id', db.Integer, primary_key = True)
   sensor = db.Column(db.String(100))
   reading_type = db.Column(db.String(50))
   reading_value = db.Column(db.String(50))
   timestamp = db.Column(db.String(50))

   def __init__(self, sensor, reading_type, reading_value, timestamp):
   	self.sensor = sensor
	self.reading_type = reading_type
	self.reading_value = reading_value
	self.timestamp = timestamp

   @property
   def serialize(self):
        return {
            'sensor': self.sensor, 
            'reading_type': self.reading_type,
            'reading_value': self.reading_value,
            'timestamp': self.timestamp
        }


@app.route('/reading', methods = ['GET', 'POST'])
@auth.login_required
def manage_readings():
	if request.method == 'POST':
		reading = request.get_json(force=True)
		timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		reading = Reading(reading['sensor'], reading['reading_type'], reading['reading_value'], timestamp)
		db.session.add(reading)
         	db.session.commit()
		return reading.sensor, 200
	elif request.method == 'GET':
		return jsonify(readings = [i.serialize for i in Reading.query.all()])
		
		
		
		


@app.route('/')
@auth.login_required
def welcome():
    return 'Smart Classroom Project'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,host='0.0.0.0')
