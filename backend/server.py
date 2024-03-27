"""
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
Name            : server.py
Assignment      : Lab 10, Exercise A, B, C
Author(s)       : Soummadip Sarkar, Mathew Roxas
Submission      : March 27th, 2024
Description     : Flask
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import datetime

app = Flask(__name__)
CORS(app)

def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)['products']

def save_products(products):
    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)

@app.route('/products', methods=['GET'])
@app.route('/products/<int:product_id>', methods=['GET'])
def get_products(product_id=None):
    products = load_products()
    if product_id is None:
        return jsonify({"products": products})
    else:
        product = next((p for p in products if p['id'] == product_id), None)
        return jsonify(product) if product else ('', 404)

@app.route('/products/add', methods=['POST'])
def add_product():
    new_product = request.json
    products = load_products()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    save_products(products)
    return jsonify(new_product), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    products = load_products()
    for product in products:
        if product['id'] == product_id:
            product.update(request.json)
            save_products(products)
            return jsonify(product)
    return ('', 404)

@app.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    products = load_products()
    for product in products:
        if product['id'] == product_id:
            product['isDeleted'] = True
            product['deletedOn'] = datetime.datetime.now().isoformat()
            save_products(products)
            return jsonify(product)
    return ('', 404)

@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

if __name__ == '__main__':
    app.run(debug=True)