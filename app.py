from flask import Flask
from flask_cors import CORS

from gateway import \
    ExceptionHandling

app = Flask(__name__)

app_context = app.app_context()
app_context.push()

cors = CORS(app)

urlBaseReports_incidents = 'http://incidents:4001'

@app.route('/report-incidents', methods=['POST','GET','PUT'])
def reports_incidents():
    return ExceptionHandling.communicate_to_microservice(ExceptionHandling, urlBaseReports_incidents + "/")
    

@app.errorhandler(404)
def resource_not_found(error):
    return ExceptionHandling.get_message_not_found_url(ExceptionHandling)

if __name__ == '__main__':
    app.run(port=4000)
