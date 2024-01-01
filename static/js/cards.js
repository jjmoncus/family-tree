// HTML for a card
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

// load cards into all card-containers once all other stuff is loaded
document.addEventListener("DOMContentLoaded", function () {
    const cardContainers = document.getElementsByClassName("card-container");

    Array.from(cardContainers).forEach(function(container) {

        const personId = container.getAttribute("person-id") || "";
        const first_name = container.getAttribute("person-first_name") || "";
        const middle_name = container.getAttribute("person-middle_name") || "";
        const last_name = container.getAttribute("person-last_name") || "";
        const nick_name = container.getAttribute("person-nick_name") || "";
        
        container.innerHTML = cardHTML(
            personId, 
            first_name,
            last_name, 
            nick_name);
      });
})

// filter cards as search input changes
function filterCards() {
    const searchInput = document.getElementById('searchInput');
    const searchTerm = searchInput.value.toLowerCase();

    const cardContainers = document.getElementsByClassName('card-container');

    Array.from(cardContainers).forEach(function (container) {

        const firstName = container.getAttribute('person-first_name').toLowerCase() || '';
        const middleName = container.getAttribute('person-middle_name').toLowerCase() || '';
        const lastName = container.getAttribute('person-last_name').toLowerCase() || '';
        const nickName = container.getAttribute('person-nick_name').toLowerCase() || '';

        const fullAndNickName = `${firstName} ${middleName} ${lastName} ${nickName}`;

        if (fullAndNickName.includes(searchTerm)) {
            container.style.display = 'inline-flex'; // inline-flex is the appropriate display setting for cards for now

        } else {
            container.style.display = 'none';
        }
    });
}
