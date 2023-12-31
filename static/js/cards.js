/*
function cardHTML(personId = 0, first_name = "", last_name = "", nick_name = "") {
    
    // card inputs
    const formHTML = `
    <div class="card">
        <a class="card-link" href="/focus/${personId}">
            <div class="card-content">
                <img src="{{ url_for('static', filename='logos/empty-prof-pic.png') }}" alt="Profile Picture">
                {% if ${nick_name} == "" %} 
                <h3>${first_name} ${last_name}</h3>
                {% else %} 
                <h3>${nick_name} ${last_name}</h3>
                {% endif %}
                <div class="icon-btn-container">
                    <a href="/delete/${personId}" class="icon-btn">
                        X
                        <!--<img src="{{ url_for('static', filename='logos/x.png') }}" alt="Delete">-->
                    </a>
                    <a class="icon-btn updateBtn">
                    E
                        <!--<img src="{{ url_for('static', filename='logos/edit.png') }}" alt="Edit">-->
                    </a>
                    <div class="formContainer" id="updateFormContainer"></div>
                    <a href="/big_card/${personId}" class="icon-btn">
                        R
                        <!--<img src="{{ url_for('static', filename='logos/read.png') }}" alt="Read">-->
                    </a>
                </div>
            </div>
        </a>
    </div>
    `;

    return formHTML
}  
*/
function cardHTML(personId = 0, first_name = "", last_name = "", nick_name = "") {
    // Create card container
    const cardContainer = document.createElement("div");
    cardContainer.classList.add("card");

    // Create card link
    const cardLink = document.createElement("a");
    cardLink.classList.add("card-link");
    cardLink.href = `/focus/${personId}`;

    // Create card content
    const cardContent = document.createElement("div");
    cardContent.classList.add("card-content");

    // Create image element
    const img = document.createElement("img");
    img.src = `/static/logos/empty-prof-pic.png`;
    img.alt = "Profile Picture";

    // Append image to card content
    cardContent.appendChild(img);

    // Create h3 element
    const h3 = document.createElement("h3");
    h3.textContent = nick_name ? `${nick_name} ${last_name}` : `${first_name} ${last_name}`;

    // Append h3 to card content
    cardContent.appendChild(h3);

    // Create icon button container
    const iconBtnContainer = document.createElement("div");
    iconBtnContainer.classList.add("icon-btn-container");

    // Create delete button
    const deleteBtn = document.createElement("a");
    deleteBtn.classList.add("icon-btn");
    deleteBtn.href = `/delete/${personId}`;
    deleteBtn.textContent = "X";

    // Create update button
    const updateBtn = document.createElement("a");
    updateBtn.classList.add("icon-btn", "updateBtn");
    updateBtn.textContent = "E";
    updateBtn.setAttribute("personId", personId);

    //Rethinkiing this approach
    // instead of having a new form container for every card
    // there will be one formContainer somewhere in the DOM
    // and we just populate it with their information and edit action route
    
    // -- Create dynamic form insert
    // -- const updateFormContainer = document.createElement("div");
    // -- updateFormContainer.classList.add("form-container");
    // -- updateFormContainer.classList.add("updateFormContainer");
    // -- updateFormContainer.setAttribute("personId", personId);
    

    // Create read button
    const readBtn = document.createElement("a");
    readBtn.classList.add("icon-btn");
    readBtn.href = `/big_card/${personId}`;
    readBtn.textContent = "R";

    // Append buttons to icon button container
    iconBtnContainer.appendChild(deleteBtn);
    iconBtnContainer.appendChild(updateBtn);
    iconBtnContainer.appendChild(readBtn);

    // Append icon button container to card content
    cardContent.appendChild(iconBtnContainer);

    // Append card content to card link
    cardLink.appendChild(cardContent);

    // Append card link to card container
    cardContainer.appendChild(cardLink);

    // Convert the generated HTML elements to a string
    const cardHTMLString = cardContainer.outerHTML;

    return cardHTMLString;
}



// load cards wherever appropriate
document.addEventListener("DOMContentLoaded", function () {
    const cardContainers = document.getElementsByClassName("card-container");

    Array.from(cardContainers).forEach(function(container) {

        const personId = container.getAttribute("person-id") || "";
        const first_name = container.getAttribute("person-first_name") || "";
        const last_name = container.getAttribute("person-last_name") || "";
        const nick_name = container.getAttribute("person-nick_name") || "";
        container.innerHTML = cardHTML(
            personId, 
            first_name,
            last_name, 
            nick_name);
      });
})
