# ----------------------------------------------------------- #
# ------------------------- Imports ------------------------- #
# ----------------------------------------------------------- #

from flask import Flask, render_template, url_for, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from sqlalchemy.orm import asdict
from datetime import datetime
# for string manipulation (analogous to `stringr`)
import re

app = Flask(__name__)
app.secret_key = b'here is a string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)














# ----------------------------------------------------------- #
# ------------------------- Models -------------------------- #
# ----------------------------------------------------------- #

# Association Tables for people
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

# Association table for stories and people involved
story_person_association = db.Table(
    'story_person_association',
    db.Column('story_id', db.Integer, db.ForeignKey('story.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'))
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
    
     # Define the many-to-many relationship between persons and stories they tell
    stories_told = db.relationship('Story', backref='teller', lazy='select')

    # Define the many-to-many relationship between persons and stories they are mentioned in
    stories_mentioned_in = db.relationship('Story',
                                           secondary=story_person_association,
                                           backref='mentioned_people',
                                           lazy='select')

    def __repr__(self):
        return '<Person %r>' % self.id
    
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key to link a story to the person who told it
    teller_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)























# ----------------------------------------------------------- #
# ---------------------- Getting pages ---------------------- #
# ----------------------------------------------------------- #

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


@app.route('/big_card/<int:id>', methods=['GET'])
def big_card(id):
    
    person = Person.query.get_or_404(id)

    # just render the big_card page, i.e. a page just showing the info
    # for `person`
    return render_template('big_card.html', person=person)

@app.route('/relationships', methods=['GET'])
def relationships():

    # sort the table by date created
    people = Person.query.order_by(Person.date_created).all()
    # render the main webpage, passing the ordered table as an object to be used in loops
    return render_template('relationships.html', people=people)

@app.route('/cancel', methods=['GET'])
def cancel():
    
    # render wherever you just were
    return redirect(request.referrer)


@app.route('/focus/<int:id>', methods=['GET'])
def focus(id):
    
    person = Person.query.get_or_404(id)

    parents = person.parents
    siblings = person.siblings
    children = person.children

    all_siblings = siblings + [person]

    people_table = Person.query.order_by(Person.date_created).all()
    parents_table = Person.query.filter(Person.id.in_([parent.id for parent in parents])).distinct().all()
    # need to be able to sort siblings_table so that 'person' is in the middle, somehow
    siblings_table = Person.query.filter(Person.id.in_([sibling.id for sibling in all_siblings])).distinct().all()
    children_table = Person.query.filter(Person.id.in_([child.id for child in children])).distinct().all()


    return render_template('focus.html', person=person, parents=parents_table, 
                           siblings=siblings_table, children=children_table, 
                           people=people_table)


























# ----------------------------------------------------------- #
# --------------- Getting data from backend ----------------- #
# ----------------------------------------------------------- #
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





















# ----------------------------------------------------------- #
# --------------- Submitting data to backend ---------------- #
# ----------------------------------------------------------- #

def add_person(form):

    # get data from form
    first_name = form['first_name']
    last_name = form['last_name']
    middle_name = form['middle_name']
    nick_name = form['nick_name']

    # pass form data to new class instance
    new_person = Person(first_name = first_name,
                        last_name = last_name,
                        middle_name = middle_name,
                        nick_name = nick_name)

    try:
        db.session.add(new_person)
        db.session.commit()
        return new_person
    except:
        return 'Error in add_person(): There was an issue adding your person'
    
def update_person(person, form):
    
    # set class instance's attributes to those from form
    person.first_name = form['first_name']
    person.last_name = form['last_name']
    person.middle_name = form['middle_name']
    person.nick_name = form['nick_name']

    try:
        db.session.commit()
        return person
    except:
        return 'Error in update_person(): There was an issue updating your person'

def connect_sibling(person_1, person_2):
    if person_1 not in person_2.siblings and person_1 != person_2:
        person_2.siblings.append(person_1)
        person_1.siblings.append(person_2)

def disconnect_sibling(person_1, person_2):
    if person_1 in person_2.siblings:
        person_2.siblings.remove(person_1)
        person_1.siblings.remove(person_2)


def sibling_logic(action, person_1, person_2):
    already_1_siblings = person_1.siblings
    already_2_siblings = person_2.siblings

    if action == "Connect":
        connect_sibling(person_1, person_2)
        for sibling in already_1_siblings:
            connect_sibling(sibling, person_2)
        for sibling in already_2_siblings:
            connect_sibling(sibling, person_1)
    elif action == "Disconnect":
        disconnect_sibling(person_1, person_2)
        for sibling in already_1_siblings:
            disconnect_sibling(sibling, person_2)
        for sibling in already_2_siblings:
            disconnect_sibling(sibling, person_1)


def parent_logic(action, parent, child): 
    
    if action == "Connect":
        # if parent is already in parent list, do nothing,
        # if not, append to parent list
        if parent not in child.parents and parent != child: 
            # submit parenthood
            child.parents.append(parent)
            
        # else:
            # eventually message that the person had already been added in the past
            # but do no db changes

    if action == "Disconnect":

        if parent in child.parents:
            # submit parenthood
            child.parents.remove(parent)
        # else:
            # eventually message that person was not a parent in the first place



@app.route('/delete/<int:id>')
def delete(id):
    
    person_to_delete = Person.query.get_or_404(id)

    try:
        db.session.delete(person_to_delete)
        db.session.commit()
        return redirect(request.referrer)
    except:
        return 'Error at /delete/<int:id>: There was a problem deleting that person'


@app.route('/table', methods=['POST', 'GET'])
def table():
    if request.method == 'POST':
        
        try:
            add_person(request.form)
            return redirect('/')
        except:
            return 'Error at /table: There was an issue adding your person'
        
    # this is thus the 'GET' case
    else:
        # sort the table by date created
        people = Person.query.order_by(Person.date_created).all()
        # render the main webpage, passing the ordered table as an object to be used in loops
        return render_template('table.html', people=people)


@app.route('/parent_child_action', methods=['POST'])
def parent_child_action():

    # get data from form
    parent_info = request.form['parent']
    parent_id = re.search("\d+", parent_info).group()
    child_info = request.form['child']
    child_id = re.search("\d+", child_info).group()
    
    # pull People objects from database
    parent = Person.query.filter_by(id = parent_id).first() # should just return one
    child = Person.query.filter_by(id = child_id).first()

    parent_logic(action = request.form['action'], parent = parent, child = child)

    db.session.commit()
    return redirect('/relationships')



@app.route('/sibling_action', methods=['POST'])
def sibling_action():

    # get data from form
    person_1_info = request.form['sibling_1']
    person_1_id = re.search("\d+", person_1_info).group()
    person_2_info = request.form['sibling_2']
    person_2_id = re.search("\d+", person_2_info).group()
    
    # pull People objects from database
    person_1 = Person.query.filter_by(id = person_1_id).first() # should just return one
    person_2 = Person.query.filter_by(id = person_2_id).first()

    sibling_logic(action = request.form['action'], person_1 = person_1, person_2 = person_2)

    db.session.commit()
    return redirect(request.referrer)



@app.route('/connect/sibling/<int:id>', methods=['POST'])
def connect2_sibling(id):
    
    # get data from form
    sibling_info = request.form['sibling']
    sibling_id = re.search("\d+", sibling_info).group()

    sibling = Person.query.filter_by(id = sibling_id).first() # should just return one
    person = Person.query.get_or_404(id)

    sibling_logic(action = request.form['action'], person_1 = sibling, person_2 = person)

    db.session.commit()
    return redirect(request.referrer)

@app.route('/connect/parent/<int:id>', methods=['POST'])
def connect_parent(id):
    
    # get data from form
    parent_info = request.form['parent']
    parent_id = re.search("\d+", parent_info).group()

    parent = Person.query.filter_by(id = parent_id).first() # should just return one
    child = Person.query.get_or_404(id)

    parent_logic(action = request.form['action'], parent = parent, child = child)
    
    db.session.commit()
    return redirect(request.referrer)

@app.route('/connect/child/<int:id>', methods=['POST'])
def connect_child(id):
    # get data from form
    child_info = request.form['child']
    child_id = re.search("\d+", child_info).group()

    child = Person.query.filter_by(id = child_id).first() # should just return one
    parent = Person.query.get_or_404(id)

    parent_logic(action = request.form['action'], parent = parent, child = child)
    
    db.session.commit()
    return redirect(request.referrer)

@app.route('/add/parent/<int:id>', methods=['POST'])
def add_parent(id):
    # first, add the person to the database
    new_person = add_person(request.form)
    
    # once added, name them a parent of person
    person = Person.query.get_or_404(id)
    person.parents.append(new_person)
    db.session.commit()

    # and route back where you were
    return redirect(request.referrer)

@app.route('/add/sibling/<int:id>', methods=['POST'])
def add_sibling(id):
    # first, add the person to the database
    new_person = add_person(request.form)
    
    # once added, name them a sibling of person, and all person's previous siblings
    person = Person.query.get_or_404(id)
    already_siblings = person.siblings
    person.siblings.append(new_person)
    for sibling in already_siblings:
        sibling.siblings.append(new_person)
    db.session.commit()

    # and route back where you were
    return redirect(request.referrer)

@app.route('/add/child/<int:id>', methods=['POST'])
def add_child(id):
    # first, add the person to the database
    new_person = add_person(request.form)
    
    # once added, name them a parent of person
    person = Person.query.get_or_404(id)
    person.children.append(new_person)
    db.session.commit()

    # and route back where you were
    return redirect(request.referrer)


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    
    person = Person.query.get_or_404(id)
    
    # set class instance's attributes to those from form
    update_person(person, request.form)
    return redirect(request.referrer)



# ----------------------------------------------------------- #
# -------------------- Need to refactor --------------------- #
# ----------------------------------------------------------- #


@app.route('/update_table/<int:id>', methods=['POST', 'GET'])
def update_table(id):
    person = Person.query.get_or_404(id)

    if request.method == 'POST':
        update_person(person, request.form)
        return redirect('/table')
        
    # This is the 'GET' case
    else:
        # just render the update_table page, i.e. a page just showing the info
        # for `person` to be updated
        return render_template('update_table.html', person=person)
    




# ----------------------------------------------------------- #
# ------------------------ Run app -------------------------- #
# ----------------------------------------------------------- #


# under what circumstances would this ever change? idk
if __name__ == "__main__":
    # runs app
    app.run(port = 8000, debug = True)