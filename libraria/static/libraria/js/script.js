let stars= 
    document.getElementsByClassName("star");

function gfg(n){
    console.log(`Rating clicked: ${n}`);
    remove();
    for (let i = 0; i < n; i++){
        if (n == 1) cls = "one";
        else if (n == 2) cls = "two";
        else if (n == 3) cls = "three";
        else if (n == 4) cls = "four";
        else if (n == 5) cls = "five";
        stars[i].className = "star " + cls;
    }
}

function remove(){
    console.log("Removing previous ratings");
    let i = 0;
    while (i < 5){
        stars[i].className = "star";
        i++;
    }
}

// login
function togglePasswordVisibility(fieldId, iconId) {
    const passwordField = document.getElementById(fieldId);
    const toggleIcon = document.getElementById(iconId);

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}


// validasi new password dan confirm password
function validatePasswords(fieldPassword, fieldConfirmPassword) {
    const newPassword = document.getElementById(fieldPassword).value;
    const confirmPassword = document.getElementById(fieldConfirmPassword).value;

    if (newPassword !== confirmPassword) {
        alert('Passwords do not match! Please try again.');
        return false;
    }
    return true;
}