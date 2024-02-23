from flask import Flask
from app_resources import all_views
from flask_cors import CORS

def create_app() -> Flask:
    app = Flask(__name__, static_folder="./build/static", template_folder="./build")
    app.config.from_pyfile('./app/config.py', silent=True)
    # set CORS on the Flask API
    _ = CORS(app, resources={r"/api/*": {"origins": "*"}})
    # add all webpages
    app.register_blueprint(all_views)

    return app

app: Flask = create_app()

# serve
if __name__ == '__main__':
    app.run(host=app.config["API_SERVER_HOST"], port=app.config["API_SERVER_PORT"], debug=True)