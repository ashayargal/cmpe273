from flask import Flask, jsonify, abort, request, Response, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import mysql
from sqlalchemy.sql.expression import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@db/exp_db'
db=SQLAlchemy(app)

class Expenses(db.Model):
    __tablename__='expenses'
    id=db.Column('id',db.Integer,primary_key=True)
    name=db.Column('name',db.String(50),nullable=False)
    email=db.Column('email',db.String(50),nullable=False)
    category=db.Column('category',db.String(50),nullable=False)
    description=db.Column('description',db.String(100),nullable=False)
    link=db.Column('link',db.String(100),nullable=False)
    estimated_costs=db.Column('estimated_costs',db.String(50),nullable=False)
    submit_date=db.Column('submit_date',db.String(50),nullable=False)
    status=db.Column('status',db.String(50),nullable=False)
    decision_date=db.Column('decision_date',db.String(50),nullable=False)

    def __init__(self,name,email,category,description,link,estimated_costs,submit_date,status,decision_date):
        self.name=name
        self.email=email
        self.category=category
        self.description=description
        self.link=link
        self.estimated_costs=estimated_costs
        self.submit_date=submit_date
        self.status=status
        self.decision_date=decision_date
    def __repr__(self):
        return '{}-{}-{}-{}-{}-{}-{}-{}-{}-{}'.format(self.name,self.email,self.category,self.description,self.link,self.estimated_costs,self.submit_date,self.status,self.decision_date)

class Create_DB():
    def __init__(self,hostname):
        import sqlalchemy
        if hostname!=None:
            HOSTNAME = hostname
        DATABASE='exp_db'
        eng = sqlalchemy.create_engine('mysql://root:admin@db:3306')
        eng.execute('CREATE DATABASE IF NOT EXISTS %s'%(DATABASE))

def config_db():
    HOSTNAME = 'db'
    try:
        HOSTNAME = request.args['db']
    except:
        pass
    data = Create_DB(hostname=HOSTNAME)
    return json.dumps({'status':True})

#expenses = [
#        {
#            'id' : 1,
#            'name' : 'no Bar',
#           'email' : 'no@bar.com',
#            'category' : 'supplies|travel|training',
#            'description' : 'office use',
#            'link' : 'http://www.google.com/',
#            'estimated_costs' : '500',
#            'submit_date' : '09-17-2016',
#            'status' : 'pending',
#            'decision_date' : ''
#
#        }
#]

#@app.route('/v1/expenses', methods=['GET'])
#def get_expenses():

#    return jsonify(expenses)

@app.route('/v1/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    expense = Expenses.query.filter_by(id=expense_id).first_or_404()
    fetch={
        'name':expense.name,
        'email':expense.email,
        'category':expense.category,
        'description':expense.description,
        'link':expense.link,
        'estimated_costs':expense.estimated_costs,
        'submit_date':expense.submit_date,
        'status':expense.status,
        'decision_date':expense.decision_date
    }
    get_response=jsonify(fetch)
    get_response.status_code=200
    return get_response

@app.route('/v1/expenses', methods=['POST'])
def create_expense():
   # if not request.json or not 'name' in request.json:
    #    abort(400)
    data=request.get_json(force=True)
    name=data['name']
    email=data['email']
    category=data['category']
    description=data['description']
    link=data['link']
    estimated_costs=data['estimated_costs']
    submit_date=data['submit_date']
    status='pending'
    decision_date=""

    expense=Expenses(name,email,category,description,link,estimated_costs,submit_date,status,decision_date)
    db.session.add(expense)
    db.session.commit()

    fetch = {
        'id': expense.id,
        'name': expense.name,
        'email': expense.email,
        'category':expense.category,
        'description': expense.description,
        'link': expense.link,
        'estimated_costs': expense.estimated_costs,
        'submit_date': expense.submit_date,
        'status': 'pending',
        'decision_date': expense.decision_date
    }
    
    post_response = Response(response=json.dumps(fetch),status=201,mimetype="application/json")
    return post_response

@app.route('/v1/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    expense = Expenses.query.filter_by(id=expense_id).first_or_404()
    data=request.get_json(force=True)
    expense.estimated_costs=data['estimated_costs']
    db.session.commit()
    put_response=Response(status=202)
    return put_response


@app.route('/v1/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expenses.query.filter_by(id=expense_id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    delete_response=Response(status=204)
    return delete_response

if __name__ =='__main__':
    config_db()
    db.create_all()
    app.run(debug=True,host='0.0.0.0',port=5000)