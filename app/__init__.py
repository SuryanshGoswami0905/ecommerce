import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ecommerce.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    
    db.init_app(app)#bind the database with flask
    
   
    with app.app_context():
        from app import models
        db.create_all()

        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp,url_prefix='/api/v1/auth')

        from app.routes.products import products_bp
        app.register_blueprint(products_bp, url_prefix='/api/v1')
        
    return app