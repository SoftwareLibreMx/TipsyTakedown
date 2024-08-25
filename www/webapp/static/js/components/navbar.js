function checkIfLoggedIn() {
    if (!globalThis.user) return;

    // Hide the sign-up form and show the sign-out button
    document.getElementById('sign-up').classList.add("d-none");
    document.getElementById('sign-out').classList.remove("d-none");

    if (window.location.pathname === '/auth/login') {
        window.location.href = '/';
    }
}

document.getElementById('btn-signout').addEventListener('click', function() {
    sessionStorage.removeItem('token');
    window.location.href = '/';
});

checkIfLoggedIn();

window.onload = function() {
    console.log('loaded');
}
