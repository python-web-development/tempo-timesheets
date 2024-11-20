from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes


### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Demo Flask API"
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

@app.route('/api/worklogs', methods=['GET'])
def get_worklogs():
    print("Test")
    return jsonify(fetch_worklogs())



import requests

# Function to fetch worklogs based on the location
def fetch_worklogs():
    api_base_url = "https://api.us.tempo.io/4"  # Choose based on client location
    api_token = os.getenv('API_TOKEN')  # Your API token
    from_date = "2021-01-01"
    to_date = "2025-01-31"
    url = f"{api_base_url}/worklogs?from={from_date}&to={to_date}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        worklogs = response.json()
        return worklogs.get('results', [])
    else:
        print(f"Failed to fetch worklogs. Status Code: {response.status_code}")
        return None




if __name__ == '__main__':
    app.run(debug=True)