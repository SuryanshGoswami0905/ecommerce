import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.users import User
from app.models.products import Product
from app.models.inventory import Inventory

app = create_app()

def seed_database():
    with app.app_context():
    
        print("Creating tables...")
        db.create_all()
        
        if not User.query.filter_by(email="admin@ecommerce.com").first():
            hashed_password = generate_password_hash('admin123')
            print("Creating Admin User...")
            admin = User(username="admin_user", email="admin@ecommerce.com", password=hashed_password,is_admin=True)
            db.session.add(admin)
                
            print("Creating 5 Products with Inventory...")
            products = [
                {"name": "Laptop", "price": 1200.00, "stock": 10},
                {"name": "Smartphone", "price": 800.00, "stock": 25},
                {"name": "Headphones", "price": 150.00, "stock": 50},
                {"name": "Monitor", "price": 300.00, "stock": 15},
                {"name": "Keyboard", "price": 50.00, "stock": 100}
            ]
            
            for p in products:
                product = Product(name=p["name"], price=p["price"])
                db.session.add(product)
                db.session.flush() 
                
                inventory = Inventory(product_id=product.id, stock_count=p["stock"])
                db.session.add(inventory)
            
            db.session.commit()
            print("Seeding completed! Database is ready.")
        else:
            print("Database already seeded.")

if __name__ == "__main__":
    seed_database()

