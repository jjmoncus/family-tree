function formHTML(action = "/", personId = 0) {
    
    // form inputs
    const formHTML = `
        <div class = 'form' id="interactive-form">
            <form id="personForm" action="${action}/${personId}" method="POST">
                <div>
                    <label>First Name</label>
                    <input type="text", name='first_name', id='first_name'>    
                </div>
                <div>
                    <label>Middle Name</label>
                    <input type="text", name='middle_name', id='middle_name'>
                </div>
                <div>
                    <label>Last Name</label>
                    <input type="text", name='last_name', id='last_name'>
                </div>
                <div>
                    <label>Nick Name</label>
                    <input type="text", name='nick_name', id='nick_name'>
                </div>
                <div class="btn-container">
                    <input type="submit" class="btn" value="Add">
                    <a href="/cancel" class="btn">Cancel</a>
                </div>
            </form>
        </div>
    `;

    return formHTML
}  


// add person button
document.addEventListener("DOMContentLoaded", function () {
    const addPersonBtn = document.getElementById("addPersonBtn");
    const personFormContainer = document.getElementById("personFormContainer");

    addPersonBtn.addEventListener("click", function () {
        const personId = document.getElementById("personFormContainer").getAttribute("data-person-id") || "";
        personFormContainer.innerHTML = formHTML(action="/", personId);
        personFormContainer.style.display = "block";
    });
})

// add Parent button
document.addEventListener("DOMContentLoaded", function () {
    const addParentBtn = document.getElementById("addParentBtn");
    const parentFormContainer = document.getElementById("parentFormContainer");

    addParentBtn.addEventListener("click", function () {
        const personId = document.getElementById("parentFormContainer").getAttribute("data-person-id") || "";
        parentFormContainer.innerHTML = formHTML(action="/add_parent", personId);
        parentFormContainer.style.display = "block";
    });
})

// add Sibling button
document.addEventListener("DOMContentLoaded", function () {
    const addSiblingBtn = document.getElementById("addSiblingBtn");
    const siblingFormContainer = document.getElementById("siblingFormContainer");

    addSiblingBtn.addEventListener("click", function () {
        const personId = document.getElementById("siblingFormContainer").getAttribute("data-person-id") || "";
        siblingFormContainer.innerHTML = formHTML(action="/add_sibling", personId);
        siblingFormContainer.style.display = "block";
    });
})

// add Child button
document.addEventListener("DOMContentLoaded", function () {
    const addChildBtn = document.getElementById("addChildBtn");
    const childFormContainer = document.getElementById("childFormContainer");

    addChildBtn.addEventListener("click", function () {
        const personId = document.getElementById("childFormContainer").getAttribute("data-person-id") || "";
        childFormContainer.innerHTML = formHTML(action="/add_child", personId);
        childFormContainer.style.display = "block";
    });
})