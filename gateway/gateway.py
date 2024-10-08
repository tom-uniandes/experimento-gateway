from flask import request, json, jsonify
import requests
from .queue import Queue
import logging
import os

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


message_error = "Error to send request, please try again"

class ExceptionHandling():

    def get_message_not_found_url(self):
        response = jsonify(self.get_response(404,"Resource not found, please contact with support"))
        return response, 404

    def get_response(status_code, message):
        data_response = {
            "message": message,
            "status_code": status_code
        }
        return data_response

    def communicate_to_microservice(self, event, endpoint):
        try:
            method = request.method
            body = request.get_json()
            params = request.args

            if method == "GET":
                response = requests.request(
                    method = method,
                    url = endpoint,
                    headers = request.headers,
                    data = request.get_data(),
                    params = params,
                    json = body,
                    timeout=1
                )
            else:
                response = Queue.send_message_queue(self, event, endpoint, method, params, body)
                return {}, 204

            status_code = response.status_code

    
            if status_code >= 400:
                response.raise_for_status()
            
            return json.loads(response.content), response.status_code
        
        except requests.exceptions.Timeout as e:
            logger.info("Log error: " + str(e))
            status_code = 504
            response = jsonify(self.get_response(status_code, message_error))
            return response, status_code
        
        except Exception as e:
            logger.info("Log error: " + str(e))
            status_code = 500
            response = jsonify(self.get_response(status_code, message_error))
            return response, status_code
        