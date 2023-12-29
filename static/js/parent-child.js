 // 'people' is passed as a value from backend

// Populate the parent dropdown with options
const parentDropdown = document.getElementById('parent');
people.forEach(person => {
    const option = document.createElement('option');
    option.value = person.id;
    option.text = person.first_name + person.last_name;
    parentDropdown.appendChild(option);
});

// Function to update the child dropdown based on the selected parent
function updateChildDropdown() {
    const parentId = document.getElementById('parent').value;
    const childDropdown = document.getElementById('child');

    // Clear existing options
    childDropdown.innerHTML = '';

    // Populate child dropdown with options based on the selected parent
    people.forEach(person => {
        if (person.id !== parseInt(parentId)) {
            const option = document.createElement('option');
            option.value = person.id;
            option.text = person.first_name + person.last_name;
            childDropdown.appendChild(option);
        }
    });
}

// Attach the updateChildDropdown function to the change event of the parent dropdown
document.getElementById('parent').addEventListener('change', updateChildDropdown);

// Function to handle setting the parent-child relationship (replace with your actual logic)
function setParentChildRelationship() {
    const parentId = document.getElementById('parent').value;
    const childId = document.getElementById('child').value;

    // Replace this with your logic to send the data to the server or perform other actions
    console.log(`Setting parent-child relationship: Parent ID ${parentId}, Child ID ${childId}`);
}