# app.py

from flask import Flask
from flask_cors import CORS
from database import db
from config import DevelopmentConfig
from controllers.pizzas_controllers import pizzas_bp
from controllers.toppings_controller import toppings_bp
from models.schemas import ma  
from flask_migrate import Migrate

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    
    migrate = Migrate(app, db)
    # Register blueprints
    app.register_blueprint(pizzas_bp)
    app.register_blueprint(toppings_bp)

    # Home route
    @app.route("/")
    def home():
        return "<h1>Pizza Management API</h1>"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)