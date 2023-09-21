# app.py

from flask import Flask
from routes import routes

app = Flask(__name__)

# Register the routes defined in routes.py with the app
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
