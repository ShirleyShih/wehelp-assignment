function validateForm() {
    // Get the checkbox element
    var checkbox = document.getElementById("agree-checkbox");
    
    // Check if the checkbox is checked
    if (!checkbox.checked) {
        // If checkbox is not checked, show an alert
        alert("Please check the checkbox first");
        return false; // Prevent form submission
    }

    // If checkbox is checked, allow form submission
    return true;
}

function backtohome(){
    window.location.href = "http://127.0.0.1:8000";
}

function signout(){
    window.location.href = "http://127.0.0.1:8000/signout";
}