import flask
from flask import render_template
from flask import request
app = flask.Flask(__name__)

@app.route('/')
def mainPage():
    return render_template('index.html')

@app.route('/lamp')
def basicJson():
    return render_template('lamp.html')

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

    #app.run(host='0.0.0.0', port=80, debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
