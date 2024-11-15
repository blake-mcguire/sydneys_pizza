from flask import Flask
from flask_cors import CORS
from database import db
from config import DevelopmentConfig

# Initialize Flask app and configurations
app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)

# Initialize database
db.init_app(app)

# Import and register blueprints
from controllers.toppings_controller import toppings_bp
from controllers.pizzas_controllers import pizzas_bp
app.register_blueprint(toppings_bp)
app.register_blueprint(pizzas_bp)

# Home route
@app.route("/")
def home():
    return "<h1>Pizza Management API</h1>"

# Run the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)