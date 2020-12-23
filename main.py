from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
import pickle


churnapp = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path  = os.path.join(base_dir, 'churn_recent.db')
model_path = os.path.join(base_dir, 'churn_modelo.p')

model = pickle.load(open(model_path, 'rb'))

churnapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ db_path

db = SQLAlchemy(churnapp)
ma = Marshmallow(churnapp)

@churnapp.route('/')
def home():
    return 'API for checking if a customer will churn next month. Input Account or Customer ID '

@churnapp.route('/will_churn')
def will_churn():
    acc_id = request.args.get('account_id', 'unknown')

    if acc_id != 'unknown':
        acc_details = Customer.query.filter_by(account_id = acc_id).first()
        result = customer_schema.dump(acc_details)
        l = [result["deposit"],
             result["withdrawal"],
             result["cum_balance"],
             result["prev_gdp"],
             result["unemployment"],
             result["med_income"],
             result["ave_amount"]]
        prediction = model.predict_proba([l])
        if prediction[0][1] < 0.3:
            return 'Customer will not churn'
        else:
            return 'Customer will churn'
        return str(prediction)
    else:
        result = 'Sorry not enough information'

    return str(result)

class Customer(db.Model):
    __tablename__ = 'full_active_accounts'
    account_id = Column(Integer, primary_key = True, unique = True)
    customer_id = Column(Integer, unique = True)
    deposit = Column(Float)
    withdrawal = Column(Float)
    cum_balance = Column(Float)
    prev_gdp = Column(Float)
    unemployment = Column(Float)
    med_income = Column(Float)
    ave_amount = Column(Float)

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('account_id', 'customer_id', 'amount', 'deposit', 'withdrawal', 'cum_balance',\
                  'prev_gdp', 'unemployment', 'med_income', 'ave_amount')

customer_schema = CustomerSchema()


if __name__ == '__main__':
    churnapp.run(host='0.0.0.0')


