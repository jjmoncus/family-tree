# import dependencies
from flask import Flask, jsonify, request

# defines the app as a Flask app object
# `__name__` is important - a special Python variable containing the name of the current module
app = Flask(__name__)

# In-memory data structure to store people
people = [{"id": 1, "first_name": "Ivette", "last_name": "Moncus", "parent_id": None},
{"id": 2, "first_name": "J.J.", "last_name": "Moncus", "parent_id": 1},
# Add more people as needed
]

# Helper function to find a person by ID
def find_person_by_id(person_id):
    return next((person for person in people if person["id"] == person_id), None)

@app.route('/api/people', methods=['GET', 'POST'])
def manage_people():
    if request.method == 'GET':
        return jsonify(people)

    elif request.method == 'POST':
        data = request.get_json()
        new_person_id = len(people) + 1
        new_person = {"id": new_person_id, "first_name": data['first_name'], "last_name": data['last_name'],"parent_id": data.get('parent_id')}
        people.append(new_person)
        return jsonify({'message': 'Person added successfully'})


# literally executes the app
if __name__ == '__main__':
    app.run(debug=True)

# You run the app by running this entire file
# using `python app.py`