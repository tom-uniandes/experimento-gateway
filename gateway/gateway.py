from flask import request, json, jsonify
import requests

message_error = "Error to send request"

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

    def communicate_to_microservice(self, endpoint):
        try:
            body = request.get_json()

            response = requests.request(
                method = request.method,
                url = endpoint,
                headers = request.headers,
                data = request.get_data(),
                params = request.args,
                json = body,
                timeout=1
            )

            status_code = response.status_code

    
            if status_code >= 400:
                response.raise_for_status()
            
            return json.loads(response.content), response.status_code
        
        except requests.exceptions.Timeout as e:
            status_code = 504
            response = jsonify(self.get_response(status_code, message_error))
            return response, status_code
        
        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, 'status_code', 500)
            response = jsonify(self.get_response(status_code, message_error))
            return response, status_code
        