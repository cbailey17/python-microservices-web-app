from dataclasses import dataclass

import requests
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate
from producer import publish

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/api/products')
    def index():
        return jsonify(Product.query.all())

    @app.route('/api/products/<int:id>/like', methods=['POST'])
    def like(id):
        req = requests.get('http://docker.for.mac.localhost:8000/api/user')
        json = req.json()

        try:
            productUser = ProductUser(user_id=json['id'], product_id=id)
            db.session.add(productUser)
            db.session.commit()

            print(id)
            publish('product_liked', id)
        except:
            abort(400, 'You already liked this product')

        return jsonify({
            'message': 'success'
        })

    return app


# Define a SQLAlchemy model for the "Product" table
@dataclass
class Product(db.Model):
    """
    auto increment is set to false because this is called through rabbitMQ
    and that would make the IDs different in django app
    """
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


# Start the Flask application in debug mode when executed directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
