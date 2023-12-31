from flask import Flask, render_template, url_for, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import asdict
from datetime import datetime
# for string manipulation (analogous to `stringr`)
import re

app = Flask(__name__)
app.secret_key = b'here is a string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Association Table
person_parent_association = db.Table(
    'person_parent_association',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('person.id'))
)

sibling_association = db.Table(
    'sibling_association',
    db.Column('left_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('person.id'))
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
                              backref = db.backref('children', lazy='select'))
    
    # Define the many-to-many relationship between siblings
    siblings = db.relationship('Person', 
                              secondary = sibling_association,
                              primaryjoin = id == sibling_association.c.left_id,
                              secondaryjoin = id == sibling_association.c.right_id,
                              back_populates = 'siblings', 
                              lazy='select')

    def __repr__(self):
        return '<Person %r>' % self.id



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
            return redirect(request.referrer)
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
        return redirect(request.referrer)
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

@app.route('/big_card/<int:id>', methods=['POST', 'GET'])
def big_card(id):
    person = Person.query.get_or_404(id)

    if request.method == 'POST':
        # maybe do some stuff later
        return redirect('/')
    
    # GET
    else:
        # just render the big_card page, i.e. a page just showing the info
        # for `person`
        return render_template('big_card.html', person=person)

@app.route('/relationships', methods=['GET'])
def relationships():

        # sort the table by date created
        people = Person.query.order_by(Person.date_created).all()
        # render the main webpage, passing the ordered table as an object to be used in loops
        return render_template('relationships.html', people=people)

@app.route('/parent_child_action', methods=['POST'])
def parent_child_action():

    # get data from form
    parent_info = request.form['parent']
    parent_id = re.search("\d+", parent_info).group()
    child_info = request.form['child']
    child_id = re.search("\d+", child_info).group()
    
    # pull People objects from database
    parent_person = Person.query.filter_by(id = parent_id).first() # should just return one
    child_person = Person.query.filter_by(id = child_id).first()

    action = request.form['action']

    if action == "Add":
        # if parent is already in parent list, do nothing,
        # if not, append to parent list
        if parent_person not in child_person.parents and parent_person != child_person: 
            # submit parenthood
            child_person.parents.append(parent_person)
            db.session.commit()
        # else:
            # eventually message that the person had already been added in the past
            # but do no db changes
    if action == "Remove":

        if parent_person in child_person.parents:
                
                # submit parenthood
                child_person.parents.remove(parent_person)
                db.session.commit()
            # else:
                # eventually message that person was not a parent in the first place
    
    return redirect('/relationships')

@app.route('/sibling_action', methods=['POST'])
def sibling_action():

    # get data from form
    sibling_1_info = request.form['sibling_1']
    sibling_1_id = re.search("\d+", sibling_1_info).group()
    sibling_2_info = request.form['sibling_2']
    sibling_2_id = re.search("\d+", sibling_2_info).group()
    
    # pull People objects from database
    sibling_1_person = Person.query.filter_by(id = sibling_1_id).first() # should just return one
    sibling_2_person = Person.query.filter_by(id = sibling_2_id).first()

    action = request.form['action']

    if action == "Add":
        # if parent is already in parent list, do nothing,
        # if not, append to parent list
        if sibling_1_person not in sibling_2_person.siblings and sibling_1_person != sibling_2_person:
            # submit parenthood
            sibling_2_person.siblings.append(sibling_1_person)
            sibling_1_person.siblings.append(sibling_2_person)
            db.session.commit()
        # else:
            # eventually message that the person had already been added in the past
            # but do no db changes
    if action == "Remove":

        if sibling_1_person in sibling_2_person.siblings:
        
            # submit parenthood
            sibling_2_person.siblings.remove(sibling_1_person)
            sibling_1_person.siblings.remove(sibling_2_person)
            db.session.commit()
        # else:
            # eventually message that person was not a parent in the first place

    return redirect('/relationships')

@app.route('/cancel', methods=['GET'])
def cancel():
    # 'GET'
    # render where you just were
    return redirect(request.referrer)

@app.route('/focus/<int:id>', methods=['GET'])
def focus(id):
    
    person = Person.query.get_or_404(id)

    parents = person.parents
    siblings = person.siblings
    children = person.children

    all_siblings = siblings + [person]

    parents_table = Person.query.filter(Person.id.in_([parent.id for parent in parents])).distinct().all()
    # need to be able to sort siblings_table so that 'person' is in the middle, somehow
    siblings_table = Person.query.filter(Person.id.in_([sibling.id for sibling in all_siblings])).distinct().all()
    children_table = Person.query.filter(Person.id.in_([child.id for child in children])).distinct().all()


    return render_template('focus.html', person=person, parents=parents_table, siblings=siblings_table, children=children_table)

@app.route('/add_parent/<int:id>', methods=['POST'])
def add_parent(id):
    # first, add the person to the database
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    middle_name = request.form['middle_name']
    nick_name = request.form['nick_name']

    new_person = Person(first_name = first_name,
                        last_name = last_name,
                        middle_name = middle_name,
                        nick_name = nick_name)

    try:
        db.session.add(new_person)
        db.session.commit()
    except:
        return 'There was an issue adding your person'
    
    # once added, name them a parent of person
    person = Person.query.get_or_404(id)
    person.parents.append(new_person)
    db.session.commit()

    # and route back where you were
    return redirect(request.referrer)

@app.route('/add_sibling/<int:id>', methods=['POST'])
def add_sibling(id):
    # first, add the person to the database
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    middle_name = request.form['middle_name']
    nick_name = request.form['nick_name']

    new_person = Person(first_name = first_name,
                        last_name = last_name,
                        middle_name = middle_name,
                        nick_name = nick_name)

    try:
        db.session.add(new_person)
        db.session.commit()
    except:
        return 'There was an issue adding your person'
    
    # once added, name them a parent of person
    person = Person.query.get_or_404(id)
    person.siblings.append(new_person)
    db.session.commit()

    # and route back where you were
    return redirect(request.referrer)

@app.route('/add_child/<int:id>', methods=['POST'])
def add_child(id):
    # first, add the person to the database
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    middle_name = request.form['middle_name']
    nick_name = request.form['nick_name']

    new_person = Person(first_name = first_name,
                        last_name = last_name,
                        middle_name = middle_name,
                        nick_name = nick_name)

    try:
        db.session.add(new_person)
        db.session.commit()
    except:
        return 'There was an issue adding your person'
    
    # once added, name them a parent of person
    person = Person.query.get_or_404(id)
    person.children.append(new_person)
    db.session.commit()

    # and route back where you were
    return redirect(request.referrer)


@app.route('/api/person/<int:id>', methods=['GET'])
def get_person(id):
    
    person = Person.query.get_or_404(id)
        # Sample data, replace with actual database query
    person_data = {
            'first_name': person.first_name,
            'middle_name': person.middle_name,
            'last_name': person.last_name,
            'nick_name': person.nick_name,
            # Add more fields as needed
            }
    return jsonify(person_data)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    
    person = Person.query.get_or_404(id)
    
    # set class instance's attributes to those from form
    person.first_name = request.form['first_name']
    person.last_name = request.form['last_name']
    person.middle_name = request.form['middle_name']
    person.nick_name = request.form['nick_name']

    try:
        db.session.commit()
        return redirect(request.referrer)
    except:
        return 'There was an issue updating your person'
    

# under what circumstances would this ever change? idk
if __name__ == "__main__":
    # runs app
    app.run(port = 8000, debug = True)