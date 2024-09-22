from flask import Flask
from flask_cors import CORS
import os

from gateway import \
    ExceptionHandling

app = Flask(__name__)

app_context = app.app_context()
app_context.push()

cors = CORS(app)

urlBaseReports_incidents = 'http://incidents-api:5000'

if os.environ.get("URL_BASE_INCIDENTS"):
    urlBaseReports_incidents = os.environ.get("URL_BASE_INCIDENTS")

print("URL-BASE-INCIDENTS: " + urlBaseReports_incidents)

NO_EVENT = ""
EVENT_INCIDENTS = "incident"


@app.route('/report-incidents', methods=['GET'])
def report_incidents():
    return ExceptionHandling.communicate_to_microservice(ExceptionHandling, NO_EVENT, urlBaseReports_incidents + "/incidents")
    
@app.route('/report-incident/<id>', methods=['POST','GET','PUT','DELETE'])
def report_incident(id):
    return ExceptionHandling.communicate_to_microservice(ExceptionHandling, EVENT_INCIDENTS, urlBaseReports_incidents + "/incident/{id}")
    

@app.errorhandler(404)
def resource_not_found(error):
    return ExceptionHandling.get_message_not_found_url(ExceptionHandling)

@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

if __name__ == '__main__':
    app.run(port=4000)
