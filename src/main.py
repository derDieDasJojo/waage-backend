# coding=utf-8
from flask import Flask, jsonify, request
from .entities.entity import Session, engine, Base
from .entities.products import Product, ProductSchema

# creating the Flask application
app = Flask(__name__)

# if needed, generate database schema
Base.metadata.create_all(engine)


@app.route('/products')
def get_products():
    # fetching from the database
    session = Session()
    product_objects = session.query(Product).all()

    # transforming into JSON-serializable objects
    schema = ProductSchema(many=True)
    exams = schema.dump(product_objects)

    # serializing as JSON
    session.close()
    return jsonify(exams.data)


@app.route('/products', methods=['POST'])
def add_products():
    # mount exam object
    posted_product = ProductSchema(only=('name', 'description'))\
        .load(request.get_json())

    product = Product(**posted_product.data, created_by="HTTP post request")

    # persist exam
    session = Session()
    session.add(product)
    session.commit()

    # return created exam
    new_exam = ProductSchema().dump(product).data
    session.close()
    return jsonify(new_exam), 201

# # generate database schema
# Base.metadata.create_all(engine)
#
# # start session
# session = Session()
#
# # check for existing data
# products = session.query(Product).all()
#
# if len(products) == 0:
#     # create and persist mock exam
#     python_exam = Product("Salat", "z.B. Feldsalat", "script")
#     session.add(python_exam)
#     session.commit()
#     session.close()
#
#     # reload exams
#     products = session.query(Product).all()
#
# # show existing exams
# print('### Products:')
# for product in products:
#     print(f'({product.id}) {product.name} - {product.description}')