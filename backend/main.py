from flask import Flask
from flask_cors import CORS
from extensions import db, migrate, jwt
from config import Config
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.transaction_routes import transaction_bp
from routes.misc_routes import misc_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# init DB tables
with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(transaction_bp, url_prefix='/transaction')
app.register_blueprint(misc_bp, url_prefix='/misc')

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)