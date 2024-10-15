from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

new_app = Flask(__name__)
ma = Marshmallow(new_app)
new_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://m16l2assignment_user:jaVndQdAFRwMQKNCbHC5k3IZ5JFDMber@dpg-cs782at6l47c7393anlg-a.oregon-postgres.render.com/m16l2assignment'
new_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(new_app, model_class=Base)

class Sum(Base):
    __tablename__ = 'sum'
    id: Mapped[int] = mapped_column(primary_key=True)
    num1: Mapped[int] = mapped_column(db.Integer, nullable=False)
    num2: Mapped[int] = mapped_column(db.Integer, nullable=False)
    result: Mapped[int] = mapped_column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Sum {self.id}: {self.num1} + {self.num2} = {self.result}>'

class SumSchema(ma.Schema):
    id = fields.Integer()
    num1 = fields.Integer()
    num2 = fields.Integer()
    result = fields.Integer()

sums_schema = SumSchema()

@new_app.route('/sum', methods=['GET'])
def find_all():
    sums = db.session.execute(db.select(Sum)).scalars()
    return jsonify(sums_schema.dumps(sums, many=True)), 200

@new_app.route('/sum', methods=['POST'])
def sum():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    result = num1 + num2
    return jsonify({'result': result})

# Create a new endpoint /sum/result/<int> that returns a list of sums filtered by the result of the sum.
@new_app.route('/sum/results/<int:num>', methods=['GET'])
def filter_sums(num):
    sums = db.session.execute(db.select(Sum).where(Sum.result == num)).scalars()
    return jsonify(sums_schema.dump(sums, many=True)), 200

with new_app.app_context():
    db.drop_all()
    db.create_all()
