// form raw HTML
function form(action = "/", personId = 0, first_name = "", middle_name = "", last_name = "", nick_name = "") {
    
    // Create form container
    const formContainer = document.createElement("div");
    formContainer.classList.add("form");

    // Create form element
    const form = document.createElement("form");
    form.id = "personForm";
    form.action = `${action}/${personId}`;
    form.method = "POST";

    // Create input elements
    const inputElements = [
        { type: "text", name: "first_name", id: "first_name", value: first_name, label: "First Name" },
        { type: "text", name: "middle_name", id: "middle_name", value: middle_name, label: "Middle Name" },
        { type: "text", name: "last_name", id: "last_name", value: last_name, label: "Last Name" },
        { type: "text", name: "nick_name", id: "nick_name", value: nick_name, label: "Nick Name" }
    ];

    inputElements.forEach(inputData => {
        const inputDiv = document.createElement("div");
        const label = document.createElement("label");
        label.textContent = inputData.label;
        const input = document.createElement("input");
        Object.entries(inputData).forEach(([key, value]) => {
            if (key !== "label") {
                input[key] = value;
            }
        });

        inputDiv.appendChild(label);
        inputDiv.appendChild(input);
        form.appendChild(inputDiv);
    });
    
    // Create button container
    const btnContainer = document.createElement("div");
    btnContainer.classList.add("btn-container");

    // Create submit button
    const submitBtn = document.createElement("input");
    submitBtn.type = "submit";
    submitBtn.classList.add("btn");
    submitBtn.value = "Add";

    // Create cancel button
    const cancelBtn = document.createElement("a");
    cancelBtn.href = "/cancel";
    cancelBtn.classList.add("btn");
    cancelBtn.textContent = "Cancel";

    // Append buttons to button container
    btnContainer.appendChild(submitBtn);
    btnContainer.appendChild(cancelBtn);

    // Append button container to form
    form.appendChild(btnContainer);

    // Append form to form container
    formContainer.appendChild(form);

    return formContainer;
}



// add person button
document.addEventListener("DOMContentLoaded", function () {
    const addPersonBtn = document.getElementById("addPersonBtn");
    const personFormContainer = document.getElementById("personFormContainer");

    addPersonBtn.addEventListener("click", function () {
        const personId = document.getElementById("personFormContainer").getAttribute("data-person-id") || "";
        personFormContainer.appendChild(form(action="/", personId));
        personFormContainer.style.display = "block";
    });
})

// New Parent button
document.addEventListener("DOMContentLoaded", function () {
    const addParentBtn = document.getElementById("addParentBtn");
    const parentFormContainer = document.getElementById("parentFormContainer");

    addParentBtn.addEventListener("click", function () {
        const personId = document.getElementById("parentFormContainer").getAttribute("data-person-id") || "";
        parentFormContainer.appendChild(form(action="/add_parent", personId));
        parentFormContainer.style.display = "block";
    });
})

// New Sibling button
document.addEventListener("DOMContentLoaded", function () {
    const addSiblingBtn = document.getElementById("addSiblingBtn");
    const siblingFormContainer = document.getElementById("siblingFormContainer");

    // whenever "addSibling Button" is clicked
    addSiblingBtn.addEventListener("click", function () {
        const personId = document.getElementById("siblingFormContainer").getAttribute("data-person-id") || "";
        siblingFormContainer.appendChild(form(action="/add_sibling", personId));
        siblingFormContainer.style.display = "block";
    });
})

// New Child button
document.addEventListener("DOMContentLoaded", function () {
    const addChildBtn = document.getElementById("addChildBtn");
    const childFormContainer = document.getElementById("childFormContainer");

    addChildBtn.addEventListener("click", function () {
        const personId = document.getElementById("childFormContainer").getAttribute("data-person-id") || "";
        childFormContainer.appendChild(form(action="/add_child", personId));
        childFormContainer.style.display = "block";
    });
})

async function getPersonInfo(personId) {
    try {
        const response = await fetch(`/api/person/${personId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

document.addEventListener("click", function (event) {
    const updateBtn = event.target.closest(".updateBtn");

    if (updateBtn) {
        const personId = updateBtn.getAttribute("personId");

        // create a form container  
        const updateFormContainer = document.createElement("div");
        updateFormContainer.classList.add("formContainer");
        updateFormContainer.classList.add("updateFormContainer");
        updateFormContainer.setAttribute("personId", personId);

        // Putting it next to all new_... Button for now      
        const panelContainer = document.getElementById("secondary-panel-column-container");
        panelContainer.appendChild(updateFormContainer);

        // get person's info for form
        getPersonInfo(personId)
            .then(person_info => {
                // Insert form content into container
                const form_to_add = form("/update", 
                personId, 
                person_info.first_name, 
                person_info.middle_name, 
                person_info.last_name, 
                person_info.nick_name);

                updateFormContainer.appendChild(form_to_add);
                updateFormContainer.style.display = "block";
            })
            .catch(error => {
                console.error('Error fetching person information:', error);
            });
    }
});
