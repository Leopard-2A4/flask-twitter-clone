from flask import Flask
from configuration import create_app
from routes.start import init_routes


app = create_app()

init_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)