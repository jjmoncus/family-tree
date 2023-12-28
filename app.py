from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Person(db.Model):
    
    # required
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(200), nullable = False)
    last_name = db.Column(db.String(200), nullable = False)

    # not required
    middle_name = db.Column(db.String(200), nullable = False, default='')
    nick_name = db.Column(db.String(200), nullable = False, default='')
    parent_id = db.Column(db.Integer, primary_key = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

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
        parent_id = request.form['parent_id']

        # pass form data to new class instance
        new_person = Person(first_name = first_name,
                            last_name = last_name,
                            middle_name = middle_name,
                            nick_name = nick_name,
                            parent_id = parent_id)

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
        person.parent_id = request.form['parent_id']


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
        person.parent_id = request.form['parent_id']


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
        parent_id = request.form['parent_id']

        # pass form data to new class instance
        new_person = Person(first_name = first_name,
                            last_name = last_name,
                            middle_name = middle_name,
                            nick_name = nick_name,
                            parent_id = parent_id)

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
    
    # 'GET'
    else:
        # just render the card_focus page, i.e. a page just showing the info
        # for `person`
        return render_template('card_focus.html', person=person)



# under what circumstances would this ever change? idk
if __name__ == "__main__":
    # runs app
    app.run(port = 8000, debug = True)