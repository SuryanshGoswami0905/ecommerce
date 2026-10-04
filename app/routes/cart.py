from flask import Blueprint, request, jsonify
from app import db
from app.models.carts import Cart
from app.models.cart_items import CartItem
from app.models.products import Product
from app.models.inventory import Inventory

cart_bp = Blueprint('cart', __name__)



@cart_bp.route('/cart/items', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')


    if not user_id or not product_id or not quantity:
        return jsonify({"error": "user_id, product_id, quantity required"}), 400

    if quantity <= 0:
        return jsonify({"error": "Quantity must be positive"}), 400


    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404


    inventory = Inventory.query.filter_by(product_id=product_id).first()
    if not inventory or inventory.stock_count < quantity:
        return jsonify({"error": "Not enough stock"}), 400


    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.flush()


    existing_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product_id
    ).first()

    if existing_item:
    
        existing_item.quantity += quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(new_item)

    db.session.commit()
    return jsonify({"message": "Item added to cart"}), 201


# Cart dekho
@cart_bp.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({"message": "Cart is empty", "items": []}), 200

    items = CartItem.query.filter_by(cart_id=cart.id).all()

    result = []
    total = 0
    for item in items:
        product = Product.query.get(item.product_id)
        subtotal = product.price * item.quantity
        total += subtotal
        result.append({
            "cart_item_id": item.id,
            "product_id": product.id,
            "product_name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return jsonify({"items": result, "total": total}), 200


# Cart se item hatao
@cart_bp.route('/cart/items/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):

    item = CartItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item removed"}), 200