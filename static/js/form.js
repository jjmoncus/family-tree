document.addEventListener("DOMContentLoaded", function () {
    const addPersonBtn = document.getElementById("addPersonBtn");
    const formContainer = document.getElementById("formContainer");

    addPersonBtn.addEventListener("click", function () {
        displayForm();
    });

    function displayForm() {
        // form inputs
        const formHTML = `

            <div class = 'form' id="interactive-form">
                <form id="personForm" action="/" method="POST">
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
                        <a href="/" class="btn">Cancel</a>
                    </div>
                </form>
            </div>
        `;

        formContainer.innerHTML = formHTML;
        formContainer.style.display = "block";
    }  
})