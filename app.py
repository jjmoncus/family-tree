from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import asdict
from datetime import datetime
# for string manipulation (analogous to `stringr`)
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Association Table
person_parent_association = db.Table(
    'person_parent_association',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('person.id'))
)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    middle_name = db.Column(db.String(200), nullable=False, default='')
    nick_name = db.Column(db.String(200), nullable=False, default='')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Define the many-to-many relationship between parents and children
    parents = db.relationship('Person', 
                              secondary = person_parent_association,
                              primaryjoin = id == person_parent_association.c.person_id,
                              secondaryjoin = id == person_parent_association.c.parent_id,
                              backref = db.backref('children', lazy='dynamic'))

    def __repr__(self):
        return '<Person %r>' % self.id
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}




@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        
        # get data from form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        nick_name = request.form['nick_name']

        # pass form data to new class instance
        new_person = Person(first_name = first_name,
                            last_name = last_name,
                            middle_name = middle_name,
                            nick_name = nick_name)

        try:
            db.session.add(new_person)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your person'
        
    # this is thus the 'GET' case
    else:
        # sort the table by date created
        people = Person.query.order_by(Person.date_created).all()
        # render the main webpage, passing the ordered table as an object to be used in loops
        return render_template('index.html', people=people)


@app.route('/delete/<int:id>')
def delete(id):
    person_to_delete = Person.query.get_or_404(id)

    try:
        db.session.delete(person_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that person'


@app.route('/update_table/<int:id>', methods=['POST', 'GET'])
def update_table(id):
    person = Person.query.get_or_404(id)

    if request.method == 'POST':
        # set class instance's attributes to those from form
        person.first_name = request.form['first_name']
        person.last_name = request.form['last_name']
        person.middle_name = request.form['middle_name']
        person.nick_name = request.form['nick_name']


        try:
            db.session.commit()
            return redirect('/table')
        except:
            return 'There was an issue updating your person'
    # This is the 'GET' case
    else:
        # just render the update_table page, i.e. a page just showing the info
        # for `person` to be updated
        return render_template('update_table.html', person=person)
    


@app.route('/update_tree/<int:id>', methods=['POST', 'GET'])
def update_tree(id):
    person = Person.query.get_or_404(id)

    if request.method == 'POST':
        # set class instance's attributes to those from form
        person.first_name = request.form['first_name']
        person.last_name = request.form['last_name']
        person.middle_name = request.form['middle_name']
        person.nick_name = request.form['nick_name']


        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your person'
    # This is the 'GET' case
    else:
        # just render the update_tree page, i.e. a page just showing the info
        # for `person` to be updated
        return render_template('update_tree.html', person=person)

@app.route('/table', methods=['POST', 'GET'])
def table():
    if request.method == 'POST':
        
        # get data from form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        nick_name = request.form['nick_name']

        # pass form data to new class instance
        new_person = Person(first_name = first_name,
                            last_name = last_name,
                            middle_name = middle_name,
                            nick_name = nick_name)

        try:
            db.session.add(new_person)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your person'
        
    # this is thus the 'GET' case
    else:
        # sort the table by date created
        people = Person.query.order_by(Person.date_created).all()
        # render the main webpage, passing the ordered table as an object to be used in loops
        return render_template('table.html', people=people)


@app.route('/card_focus/<int:id>', methods=['POST', 'GET'])
def card_focus(id):
    person = Person.query.get_or_404(id)

    if request.method == 'POST':
        # maybe do some stuff later
        return redirect('/')
    
    # GET
    else:
        # just render the card_focus page, i.e. a page just showing the info
        # for `person`
        return render_template('card_focus.html', person=person)


@app.route('/parent_child', methods=['POST', 'GET'])
def parent_child():

    if request.method == 'POST':
       
        # get data from form
        parent_info = request.form['parent']
        parent_id = re.search("\d+", parent_info).group()
        child_info = request.form['child']
        child_id = re.search("\d+", child_info).group()
        
        # pull People objects from database
        parent_person = Person.query.filter_by(id = parent_id).first() # should just return one
        child_person = Person.query.filter_by(id = child_id).first()

        # submit parenthood
        child_person.parents.append(parent_person)
        db.session.commit()
        return redirect('/parent_child')
    
    # GET
    else:
        # sort the table by date created
        people = Person.query.order_by(Person.date_created).all()
        # render the main webpage, passing the ordered table as an object to be used in loops
        return render_template('parent_child.html', people=people)



# under what circumstances would this ever change? idk
if __name__ == "__main__":
    # runs app
    app.run(port = 8000, debug = True)