# coding=utf-8

from .entities.entity import Session, engine, Base
from .entities.products import Product

# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check for existing data
products = session.query(Product).all()

if len(products) == 0:
    # create and persist mock exam
    python_exam = Product("Salat", "z.B. Feldsalat", "script")
    session.add(python_exam)
    session.commit()
    session.close()

    # reload exams
    products = session.query(Product).all()

# show existing exams
print('### Products:')
for product in products:
    print(f'({product.id}) {product.name} - {product.description}')