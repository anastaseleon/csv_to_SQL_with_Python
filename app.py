from flask import Flask, render_template
from flask_cors import CORS
from routes.transaction_routes import bp as transaction_bp
from routes.uploaded_files import bp as uploaded_files_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(transaction_bp)
app.register_blueprint(uploaded_files_bp)

@app.route('/')
def index():
    return render_template('index.html')  # This serves your index.html

if __name__ == "__main__":
    app.run(debug=True)
