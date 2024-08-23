from flask import Flask
from flask_cors import CORS
from routes.import_routes import bp as import_bp
from routes.transaction_routes import bp as transaction_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(import_bp)
app.register_blueprint(transaction_bp)

if __name__ == "__main__":
    app.run(debug=True)
