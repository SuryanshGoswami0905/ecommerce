from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from app import db
from app.models.users import User
from app.models.wallets import Wallet

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():                                    
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Username, email and password needed!"}), 400


    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "This E-mail already exist!"}), 409

    
    hashed_password = generate_password_hash(password)

    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    
    
    db.session.flush() 

    new_wallet = Wallet(user_id=new_user.id, balance=0.0)
    db.session.add(new_wallet)

    db.session.commit()

    
    return jsonify({"message": "User and Wallet successfully created!"}), 201


@auth_bp.route('/login',methods=['POST'])
def login():                                    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password needed!"}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if check_password_hash(user.password , password):
        return jsonify({"message": "Login successful",
                "user_id": user.id,
             "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin
            }), 200
    else:
        return jsonify({"error": "Wrong password"}), 401
    
    

