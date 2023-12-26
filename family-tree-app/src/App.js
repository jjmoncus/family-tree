import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

// ... (existing code)

function App() {
  const [people, setPeople] = useState([]);
  const [newPerson, setNewPerson] = useState({ first_name: '', last_name: '' });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewPerson({ ...newPerson, [name]: value });
  };

  // this is apparently working as appropriate
  const handleFormSubmit = (e) => {
    e.preventDefault();
    axios.post('/api/people', newPerson)
      .then(response => {
        console.log(response.data.message);
        // Optionally, you can refresh the list of people after adding a new one
        axios.get('/api/people')
          .then(response => {
            setPeople(response.data)
            console.log('New people data:', response.data);
          })
          .catch(error => console.error('Error fetching data:', error));
      })
      .catch(error => console.error('Error adding person:', error));

      console.log('Form submitted!')
  };

  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    setLoading(true); // Set loading state to true before the request

    axios.get('/api/people')
      .then(response => {
        setPeople(response.data);
        setLoading(false); // Set loading state to false after successful request
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false); // Set loading state to false after error
      });
  }, []);


  return (
    <div className="App">
      <h1>Family Tree</h1>
      <form onSubmit={handleFormSubmit}>
        <label>
          First Name:
          <input type="text" name="first_name" value={newPerson.first_name} onChange={handleInputChange} required />
        </label>
        <label>
          Last Name:
          <input type="text" name="last_name" value={newPerson.last_name} onChange={handleInputChange} required />
        </label>
        <button type="submit">Submit</button>
      </form>
      <div className="card-container">
        {people.map(person => (
          <div key={person.id} className="card">
            <p>{person.first_name} {person.last_name}</p>
            <p>Parent ID: {person.parent_id}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

// ... (existing code)

export default App;
