from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import sqlite3

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lampy.sqlite3'
lampy = SQLAlchemy(app)

def describeTable():
    con = sqlite3.connect("lampy.sqlite3")
    cur = con.cursor()
    cur.execute("PRAGMA table_info(lamp)")
    temp = cur.fetchall()
    ret = []
    for i in temp:
        ret.append(i[1])
    return ret
# get an updated list of column names
lampDescription = describeTable()

def describeAlarmTable():
    con = sqlite3.connect("lampy.sqlite3")
    cur = con.cursor()
    cur.execute("PRAGMA table_info(alarm)")
    temp = cur.fetchall()
    ret = []
    for i in temp:
        ret.append(i[1])
    return ret

alarmDescription = describeAlarmTable()

# lamp object
class lamp(lampy.Model):
    _id = lampy.Column("id", lampy.Integer, primary_key=True)
    toggle = lampy.Column(lampy.Boolean, nullable=False)
    lock = lampy.Column(lampy.Boolean, nullable=False)
    extra = lampy.Column(lampy.String(20))
    brightness = lampy.Column(lampy.Integer, nullable=False)
    red = lampy.Column(lampy.Integer, nullable=False)
    blue = lampy.Column(lampy.Integer, nullable=False)
    green = lampy.Column(lampy.Integer, nullable=False)

class alarm(lampy.Model):
    _id = lampy.Column("id", lampy.Integer, primary_key=True)
    toggle = lampy.Column(lampy.Boolean, nullable=False)
    duration = lampy.Column(lampy.Integer, nullable=False)
    time = lampy.Column(lampy.Integer, nullable=False)
    maxBrightness = lampy.Column(lampy.Integer, nullable=False)
    triggerScript = lampy.Column(lampy.Boolean, nullable=False)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
def mainPage():
    return render_template('index.html')

@app.route('/lamp')
def basicJson():
    return render_template('lamp.html')

@app.route('/lampy', methods = ['GET'])
def values():
    # uses dict_factory to createa  dict of stuff (idk how....)
    con = sqlite3.connect("lampy.sqlite3")
    con.row_factory = dict_factory
    cur = con.cursor()
    # gets row at id=1
    cur.execute("select * from lamp where id=1")
    ret = cur.fetchall()
    # gets the first instance to go from list to json
    ret = ret[0]
    con.close()
    return str(ret)

@app.route('/lampy/setValues', methods = ['POST'])
def setValues():
    data = request.json
    print("Data recieved: ")
    print(data)
    ret = ""
    con = sqlite3.connect("lampy.sqlite3")
    cur = con.cursor()
    for key in data:
        if key in lampDescription:
            if key == "extra":
                data[key] = "\'" + data[key] + "\'"
            execution = str("update lamp set " + str(key) + "=" + str(data[key]) + " where id=1")
            print(execution)
            cur.execute(execution)
            con.commit()
            ret = ret + str(key) + " was successfully updated\n"
        else:
            ret = ret + "Error: " + str(key) + " is not a recognized variable and was not updated\n"
    con.close()
    return ret

@app.route('/lampy/setAlarm', methods = ['POST'])
def setAlarm():
    data = request.json
    print("Data recieved: ")
    print(data)
    ret = ""
    con = sqlite3.connect("lampy.sqlite3")
    cur = con.cursor()
    for key in data:
        if key in alarmDescription:
            execution = str("update alarm set " + str(key) + "=" + str(data[key]) + " where id=1")
            print(execution)
            cur.execute(execution)
            con.commit()
            ret = ret + str(key) + " was successfully updated\n"
        else:
            ret = ret + "Error: " + str(key) + " is not a recognized variable and was not updated\n"
    con.close()
    return ret

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

    #app.run(host='0.0.0.0', port=80, debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
