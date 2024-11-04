import os
from apiflask import APIFlask
from flask_cors import CORS

from blueprints.stt import stt_blueprint
from blueprints.file import file_blueprint
from helpers.constants import TEMP_FOLDER

app = APIFlask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(stt_blueprint, url_prefix='/api/v1/')
app.register_blueprint(file_blueprint, url_prefix='/api/v1/')

os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route('/health', methods=['GET'])
def health_endpoint():
    return {'message': 'OK !'}

# if __name__ == '__main__': 
#     app.run(host = '127.0.0.1', port = 8080, debug = True)