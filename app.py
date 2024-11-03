import os
from apiflask import APIFlask
from flask_cors import CORS

from blueprints.stt import stt_blueprint

app = APIFlask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(stt_blueprint, url_prefix='/api/v1/')

@app.route('/health', methods=['GET'])
def health_endpoint():
    return {'message': 'OK !'}

# if __name__ == '__main__': 
#     app.run(host = '127.0.0.1', port = 8080, debug = True)