from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

# Target API URL
API_URL = "http://localhost:8000"

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
def proxy(path):
    # Forward the request to the actual API
    url = f"{API_URL}/{path}"
    
    # Get headers from the incoming request
    headers = {key: value for key, value in request.headers if key != 'Host'}
    
    # Handle OPTIONS requests for CORS preflight
    if request.method == 'OPTIONS':
        response = Response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    # Forward the request to the actual API
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        
        # Create a Flask Response object
        response = Response(resp.content)
        
        # Copy headers from the API response
        for key, value in resp.headers.items():
            if key.lower() != 'content-length':  # Skip content-length as it will be set automatically
                response.headers[key] = value
        
        # Add CORS headers
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        
        return response
    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
