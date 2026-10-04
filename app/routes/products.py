from flask import Blueprint, request, jsonify
from app import db
from app.models.products import Product
from app.models.inventory import Inventory

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    name = request.args.get('name')

    if name:
        products = Product.query.filter(Product.name.ilike(f'%{name}%')).all()
    else:
        products = Product.query.all()


    result = []
    for p in products:
       
        inventory = Inventory.query.filter_by(product_id=p.id).first()
        stock = inventory.stock_count if inventory else 0

        result.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "stock": stock
        })

    return jsonify(result), 200