from app import db

class Refund(db.Model):
    __tablename__ = 'refunds'
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='pending')