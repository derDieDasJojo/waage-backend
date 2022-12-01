# coding=utf-8
from flask import Flask, jsonify, request
from flask_cors import CORS
from .entities.entity import Session, engine, Base
from .entities.products import Product, ProductSchema
from .entities.exam import Exam, ExamSchema
from .entities.scale import Scale, ScaleSchema
from sqlalchemy import desc


EMULATE_HX711=True
if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from .hx711.hx711 import HX711
else:
    from .hx711.emulated_hx711 import HX711
# ... other import statements ...

# creating the Flask application
app = Flask(__name__)
CORS(app)

# if needed, generate database schema
Base.metadata.create_all(engine)

@app.route('/')
def get_base():
    return jsonify({'key': 'value'})

@app.route('/exams')
def get_exams():
    # fetching from the database
    session = Session()
    exam_objects = session.query(Exam).all()

    # transforming into JSON-serializable objects
    schema = ExamSchema(many=True)
    exams = schema.dump(exam_objects)

    # serializing as JSON
    session.close()
    return jsonify(exams)

@app.route('/exams', methods=['POST'])
def add_exam():
    # mount exam object
    posted_exam = ExamSchema(only=('title', 'description'))\
        .load(request.get_json())

    exam = Exam(**posted_exam, created_by="HTTP post request")

    # persist exam
    session = Session()
    session.add(exam)
    session.commit()

    # return created exam
    new_exam = ExamSchema().dump(exam)
    session.close()
    return jsonify(new_exam), 201

@app.route('/products')
def get_products():
    # fetching from the database
    session = Session()
    product_objects = session.query(Product).all()

    # transforming into JSON-serializable objects
    schema = ProductSchema(many=True)
    product = schema.dump(product_objects)

    # serializing as JSON
    session.close()
    return jsonify(product)


@app.route('/products', methods=['POST'])
def add_products():
    # mount exam object
    posted_product = ProductSchema(only=('name', 'description'))\
        .load(request.get_json())
    product = Product(**posted_product, created_by="HTTP post request")

    # persist exam
    session = Session()
    session.add(product)
    session.commit()

    # return created exam
    new_product = ProductSchema().dump(product)
    session.close()
    return jsonify(new_product), 201

@app.route('/scale/tare' , methods=['GET','POST'])
def init_scale():
    # set static values
    reference_unit = 9955

    # initialize scale
    hx = configure_hx(offset=0, reference_unit=reference_unit)
    hx.tare(30)
    offset = hx.get_offset()
    print("Tare done! Add weight now...")


    scale = Scale(offset, reference_unit,created_by="")

    # persist scale
    session = Session()
    session.add(scale)
    session.commit()

    # return created exam
    new_scale = ProductSchema().dump(scale)
    session.close()


    #return config
    return jsonify({"offset":offset,"reference_unit":reference_unit}), 201

@app.route('/scale/config')
def getConfig():
    scale = getConfigFromDB()

    return jsonify(scale)

@app.route('/scale')
def getWeight():
    scale = getConfigFromDB()
    hx = configure_hx(scale['offset'], scale['reference_unit'])
    try:
        val = hx.get_weight(9)
        print("{0:.2f} kg".format(val))
        hx.power_down()
        hx.power_up()
        #return val
        return jsonify(val), 201

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


def getConfigFromDB():
    # fetching from the database
    session = Session()
    scale_objects = session.query(Scale).order_by(desc(Scale.updated_at)).first()

    # transforming into JSON-serializable objects
    schema = ScaleSchema(many=False)
    scale = schema.dump(scale_objects)

    # serializing as JSON
    session.close()

    return scale

def configure_hx(offset, reference_unit):
    # setup AD Converter
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(reference_unit)
    hx.set_offset(offset)
    hx.reset()
    return hx

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()

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
